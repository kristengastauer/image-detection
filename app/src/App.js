import React, { useState } from 'react';
import Header from "./components/Header";
import FormPage from "./components/FormPage";
import MetaPage from "./components/MetaPage";
import LibraryPage from "./components/LibraryPage";


function App() {
  const [selectedPage, setSelectedPage] = useState("form");

  let currentPage = <FormPage setSelectedPage={setSelectedPage} />;
  if (selectedPage === "meta"){
    currentPage = <MetaPage setSelectedPage={setSelectedPage}/>;
  }

  if (selectedPage === "library") {
    currentPage = <LibraryPage setSelectedPage={setSelectedPage}/>;
  }

  return (
    <div>
      <Header selectedPage={ selectedPage } setSelectedPage={ setSelectedPage } />
        {currentPage}
    </div>
  );
}


export default App;
