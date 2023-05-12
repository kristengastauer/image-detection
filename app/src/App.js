import React, { useState } from 'react';
import Header from "./components/Header";
import FormPage from "./components/FormPage";
import MetaPage from "./components/MetaPage";


function App() {
  const [selectedPage, setSelectedPage] = useState("form");

  return (
    <div>
      <Header selectedPage={ selectedPage } setSelectedPage={ setSelectedPage } />
        {selectedPage === "meta" ? (
          <MetaPage setSelectedPage={setSelectedPage}/>
          ) : (
          <FormPage setSelectedPage={setSelectedPage} />
        )}
    </div>
  );
}


export default App;
