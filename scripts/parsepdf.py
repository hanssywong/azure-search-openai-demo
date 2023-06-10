import argparse
import glob
import json
import os
import re
from pypdf import PdfReader, PdfWriter

MAX_SECTION_LENGTH = 1000
SENTENCE_SEARCH_LIMIT = 100
SECTION_OVERLAP = 100

parser = argparse.ArgumentParser(
    description="Prepare documents by extracting content from PDFs, splitting content into sections",
    epilog="Example: prepdocs.py '..\data\*' -v"
)
parser.add_argument("files", help="Files to be processed")
parser.add_argument("--verbose", "-v", action="store_true",
                    help="Verbose output")
args = parser.parse_args()


def split_text(page_map):
    SENTENCE_ENDINGS = [".", "!", "?"]
    WORDS_BREAKS = [",", ";", ":", " ",
                    "(", ")", "[", "]", "{", "}", "\t", "\n"]
    if args.verbose:
        print(f"Splitting '{filename}' into sections")

    def find_page(offset):
        l = len(page_map)
        for i in range(l - 1):
            if offset >= page_map[i][1] and offset < page_map[i + 1][1]:
                return i
        return l - 1

    all_text = "".join(p[2] for p in page_map)
    length = len(all_text)
    start = 0
    end = length
    while start + SECTION_OVERLAP < length:
        last_word = -1
        end = start + MAX_SECTION_LENGTH

        if end > length:
            end = length
        else:
            # Try to find the end of the sentence
            while end < length and (end - start - MAX_SECTION_LENGTH) < SENTENCE_SEARCH_LIMIT and all_text[end] not in SENTENCE_ENDINGS:
                if all_text[end] in WORDS_BREAKS:
                    last_word = end
                end += 1
            if end < length and all_text[end] not in SENTENCE_ENDINGS and last_word > 0:
                end = last_word  # Fall back to at least keeping a whole word
        if end < length:
            end += 1

        # Try to find the start of the sentence or at least a whole word boundary
        last_word = -1
        while start > 0 and start > end - MAX_SECTION_LENGTH - 2 * SENTENCE_SEARCH_LIMIT and all_text[start] not in SENTENCE_ENDINGS:
            if all_text[start] in WORDS_BREAKS:
                last_word = start
            start -= 1
        if all_text[start] not in SENTENCE_ENDINGS and last_word > 0:
            start = last_word
        if start > 0:
            start += 1

        section_text = all_text[start:end]
        yield (section_text, find_page(start))

        last_table_start = section_text.rfind("<table")
        if (last_table_start > 2 * SENTENCE_SEARCH_LIMIT and last_table_start > section_text.rfind("</table")):
            # If the section ends with an unclosed table, we need to start the next section with the table.
            # If table starts inside SENTENCE_SEARCH_LIMIT, we ignore it, as that will cause an infinite loop for tables longer than MAX_SECTION_LENGTH
            # If last table starts inside SECTION_OVERLAP, keep overlapping
            if args.verbose:
                print(
                    f"Section ends with unclosed table, starting next section with the table at page {find_page(start)} offset {start} table start {last_table_start}")
            start = min(end - SECTION_OVERLAP, start + last_table_start)
        else:
            start = end - SECTION_OVERLAP

    if start + SECTION_OVERLAP < end:
        yield (all_text[start:end], find_page(start))


def blob_name_from_file_page(filename, page=0):
    if os.path.splitext(filename)[1].lower() == ".pdf":
        return os.path.splitext(os.path.basename(filename))[0] + f"-{page}" + ".pdf"
    else:
        return os.path.basename(filename)


def create_sections(filename, page_map):
    for i, (section, pagenum) in enumerate(split_text(page_map)):
        yield {
            "id": re.sub("[^0-9a-zA-Z_-]", "_", f"{filename}-{i}"),
            "content": section,
            # "category": args.category,
            "sourcepage": blob_name_from_file_page(filename, pagenum),
            "sourcefile": filename
        }


def get_document_text(filename):
    offset = 0
    page_map = []
    reader = PdfReader(filename)
    pages = reader.pages
    for page_num, p in enumerate(pages):
        page_text = p.extract_text()
        if args.verbose:
            print(
                f"page_num: {filename}, offset: {offset}, page_text: {len(page_text)}")
        page_map.append((page_num, offset, page_text))
        offset += len(page_text)
    return page_map


print(f"Processing files...")
for filename in glob.glob(args.files):
    page_map = get_document_text(filename)
    basename = os.path.basename(filename)
    sections = create_sections(basename, page_map)
    jsonfilename = os.path.basename(filename).replace(".pdf","")
    batch = []
    for s in sections:
        batch.append(s)
    with open(f'{jsonfilename}-sections.json', 'w') as outfile:
        json.dump(batch, outfile)
    # with open(f'{jsonfilename}-page_map.json', 'w') as outfile:
    #     json.dump(page_map, outfile)
