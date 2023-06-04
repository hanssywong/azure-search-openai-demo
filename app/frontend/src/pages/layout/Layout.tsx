import { Outlet, NavLink, Link } from "react-router-dom";

import styles from "./Layout.module.css";

const Layout = () => {
    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <h3 className={styles.headerTitle}>GPT + ChainStorePlus | Sample</h3>
                    </Link>
                    <nav>
                        <ul className={styles.headerNavList}>
                            <li>
                                <NavLink to="/" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                    Chat
                                </NavLink>
                            </li>
                            <li className={styles.headerNavLeftMargin}>
                                <NavLink to="/qa" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                    Ask a question
                                </NavLink>
                            </li>
                            <li className={styles.headerNavLeftMargin}>
                                <a href="https://www.chainstoreplus.com/" target={"_blank"} title="ChainStorePlus website link">
                                    <img
                                        src="https://www.chainstoreplus.com/sites/chainstoreplus/files/all-ChainStorePlus-logo-H70pxtrans_0.png"
                                        alt="CSPlus logo"
                                        aria-label="Link to ChainStorePlus website"
                                        height="20px"
                                        className={styles.githubLogo}
                                    />
                                </a>
                            </li>
                        </ul>
                    </nav>
                    <h4 className={styles.headerRightText}>ChainStorePlus POS & Backoffice</h4>
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
