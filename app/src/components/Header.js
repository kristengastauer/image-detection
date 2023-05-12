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
                        <span style={{ color: selectedPage === "form" ? "#BEBEBE" : 'white' }}>Add Image</span>
                    </li>
                    <li onClick={() => setSelectedPage("meta")}>
                        <span style={{ color: selectedPage === "meta" ? "#BEBEBE" : 'white' }}>View Meta</span>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
  );
}

export default Header;