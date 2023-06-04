import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "List modules with their descriptions, suggest follow-up questions",
        value: "List modules with their descriptions, suggest follow-up questions"
    },
    {
        text: "Detailed explanation about receive stock",
        value: "Detailed explanation about receive stock"
    },
    {
        text: "Detailed explanation about promotion and discount methods",
        value: "Detailed explanation about promotion and discount methods"
    }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
