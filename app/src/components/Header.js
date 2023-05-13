import React from 'react';
import './styles/Header.css';

function Header(props) {
  const { selectedPage, setSelectedPage } = props;
  return (
    <div className="header">
        <h1>Welcome to #image-detection</h1>
        <div>
            <nav>
                <ul>
                    <li onClick={() => setSelectedPage("form")}>
                        <span style={{ color: selectedPage === "form" ? 'white' : "#BEBEBE" }}>Add Image</span>
                    </li>
                    <li onClick={() => setSelectedPage("meta")}>
                        <span style={{ color: selectedPage === "meta" ? 'white' : "#BEBEBE" }}>View Meta</span>
                    </li>
                    <li onClick={() => setSelectedPage("library")}>
                        <span style={{ color: selectedPage === "library" ? 'white' : "#BEBEBE" }}>Library</span>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
  );
}

export default Header;