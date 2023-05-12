import React, { useState } from 'react';
import './Form.css';
import axios from "axios";
import Input from "./components/Input";

function App() {
  const options = [
    { value: "url", label: "URL" },
    { value: "file", label: "File" },
  ];

  const [imageURL, setInputValue] = useState("");
  const [labelValue, setLabelValue] = useState("");
  const [objectResponse, setObjectResponse] = useState("");
  const [imageType, setImageType] = useState(options[0].value);

  const handleURLChange = (event) => {
    setInputValue(event.target.value);
  };
  const handleLabelChange = (event) => {
    setLabelValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const imgData = new FormData();
    imgData.append("image", imageURL);
    imgData.append("image_type", imageType);
    imgData.append("label", labelValue);
    imgData.append("enable_detection", true);
    axios.post("/images", imgData)
      .then((response) => {
        setObjectResponse(JSON.stringify(response.data.image.objects, null, 0));
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div>
        <div className="form-container">
          <form onSubmit={handleSubmit}>
            <div>
              <Input text={imageURL} onChange={handleURLChange} placeholder="URL or Path" label="Image:" />
              <Input text={labelValue} onChange={handleLabelChange} placeholder="myImage" label="Image Name:" />
              <select value={imageType} onChange={(e) => setImageType(e.target.value)}>
                {options.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <div><button type="submit">Detect Objects</button></div>
            </div>
          </form>
        </div>
        {objectResponse && (
          <div className="output-container">
            {labelValue} contains the following objects:
            <pre>
              <code>{objectResponse}</code>
            </pre>
          </div>
        )}
    </div>
  );
}


export default App;
