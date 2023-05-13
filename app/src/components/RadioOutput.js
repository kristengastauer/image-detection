import React from "react";
import Loading from './LoadingComponent';
import './styles/RadioOutput.css';

function RadioOutput(props) {
    const { header, text, objects, selectedObject, handleClick, loading } = props;
    if (loading) {
        return <Loading />;
    }
    if (!objects.length) {
        return;
    }
    return (
        <div className="output-container">
            <h4>{header}</h4>
            { text }
            <form>
                {objects.map((item, _) => (
                    <div>
                        <input
                            type="radio"
                            name={item}
                            value={item}
                            checked={selectedObject === item}
                            onChange={handleClick}
                        /> {item}
                    </div>
                ))}
            </form>
        </div>
    );
};

export default RadioOutput;