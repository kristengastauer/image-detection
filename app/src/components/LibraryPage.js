import React, { Component } from 'react';
import Loading from './LoadingComponent';
import axios from "axios";

// this page is a component because i needed to use lifecycle method `componentDidMount` because i make an API call on render
class LibraryPage extends Component {

    constructor(props) {
        super(props);
    
        this.state = {
          data: null,
          loading: true
        };
      }

    componentDidMount() {
        axios.get("/images")
          .then(response => {
            this.setState({
              data: response.data.images,
              loading: false
            });
          })
          .catch(error => {
            console.log(error);
            this.setState({ loading: false });
          });
    }

    render() {
        const { data, loading } = this.state;
        if (loading) {
            return <Loading />
        }
        return (
            <div className="form-container">
                {data.map((image, _) => (
                        <div className="output-container">
                            <code>
                                <div>Id: {image.id}, Label: {image.label}, Detection Enabled: {image.enable_detection ? "True" : "False"}</div>
                                <div>Objects: {image.objects ? image.objects.map((obj, index) => (index !== image.objects.length - 1 ? obj + ", " : obj)) : "None detected"}</div>
                            </code>
                        </div>
                    ))}
            </div>
        )
    }
}


export default LibraryPage;