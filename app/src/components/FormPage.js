import React, { useState } from 'react';
import axios from "axios";
import Input from './Input';
import RadioOutput from './RadioOutput';
import './styles/Form.css'

function FormPage({ props }) {
    const options = [
        { value: "url", label: "URL" },
        { value: "file", label: "File" },
    ];

    const [imageURL, setInputValue] = useState("");
    const [labelValue, setLabelValue] = useState("");
    const [imagesResponse, setImagesResponse] = useState([]);
    const [imageLoading, setImageLoading] = useState(false);
    const [objectResponse, setObjectResponse] = useState("");
    const [imageType, setImageType] = useState(options[0].value);
    const [selectedObject, setSelectedObject] = useState("");

    const handleURLChange = (event) => {
        setInputValue(event.target.value);
    };
    const handleLabelChange = (event) => {
        setLabelValue(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        setImageLoading(true);
        const imgData = new FormData();
        imgData.append("image", imageURL);
        imgData.append("image_type", imageType);
        imgData.append("label", labelValue);
        imgData.append("enable_detection", true);
        axios.post("/images", imgData)
            .then((response) => {
                const imageObjs = response.data.image.objects
                setImageLoading(false);
                setImagesResponse(imageObjs ? imageObjs : []);
            })
            .catch((error) => {
                setImageLoading(false);
                console.log(error);
            });
    };

    const handleClick = (event) => {
        event.preventDefault();
        setSelectedObject(event.target.value);
        axios.get('/images?objects=' + event.target.value)
            .then((response) => {
                setObjectResponse(response.data.images);
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
            <RadioOutput 
                loading={imageLoading}
                header={`Objects detected in Image ${labelValue}:`}
                text="Select an object to see other images that contain it"
                objects={imagesResponse}
                selectedObject={selectedObject}
                handleClick={handleClick} />
            {objectResponse &&
                <div className="output-container">
                    <code>
                        {objectResponse.map((image, index) => (
                            index !== objectResponse.length - 1 ? 
                                image.id + "," : image.id
                        ))}
                    </code>
                </div>
            }
        </div>
    )
}

export default FormPage;