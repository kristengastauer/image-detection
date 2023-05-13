import React, { useState } from 'react';
import Input from './Input';
import axios from "axios";

function MetaPage({ props }) {
    const [imageResponse, setImageResponse] = useState("");
    const [imageId, setSelectedImage] = useState("");
  

    const handleIdChange = (event) => {
        setSelectedImage(event.target.value);
    };
    const handleSubmit = (event) => {
        event.preventDefault();
        axios.get("/images/" + imageId )
            .then((response) => {
                setImageResponse(response.data.image);
            })
            .catch((error) => {
                console.log(error);
            });
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit}>
                <Input text={imageId} onChange={handleIdChange} placeholder="Image Id" label="Image Id:" />
                <div><button type="submit">Get Meta</button></div>
            </form>
            {
                imageResponse && (
                    <div className="output-container">
                        <code>
                            Id: {imageResponse.id}, Label: {imageResponse.label}, Detection Enabled: {imageResponse.enable_detection ? "True": "False"},
                            Objects: {
                                imageResponse.objects.map((obj, index) => (index !== imageResponse.objects.length - 1 ? obj + ", " : obj))
                            }
                        </code>
                    </div>
                )
            }
        </div>
    )
}


export default MetaPage;