import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import './style.css';

function App() {
  const [imageURLs, setImageURLs] = useState([]);
  const [outputImages, setOutputImages] = useState([]);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await axios.get('http://45.9.25.190:8000/list-images/');
        const images = response.data.split('<br>');
        setImageURLs(images);
      } catch (error) {
        console.error('Error fetching image URLs', error);
      }
    };

    fetchImages();
  }, []);

  useEffect(() => {
    const fetchOutputImages = async () => {
      try {
        const response = await axios.get('http://45.9.25.190:8000/output/');
        const images = response.data.images;
        setOutputImages(images);
      } catch (error) {
        console.error('Error fetching output images', error);
      }
    };

    fetchOutputImages();
  }, []);

  const [imageURL, setImageURL] = useState(null);
  const [outputImageURL, setOutputImageURL] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const result = imageURL ? '/output' + imageURL.replace('/images', '') : '';

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://45.9.25.190:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const uploadedImageURL = response.data.image_url;
      const outputImageURL = response.data.output_image_url;

      setImageURL(uploadedImageURL);
      setOutputImageURL(outputImageURL);
      setSelectedFile(null);
    } catch (error) {
      console.error('Ошибка при загрузке изображения', error);
    }
  };

  return (
    <div className="App">
      <Header />
      <div className="rectangle-container">


          <div className="rectangle rectangle-button">
            <label className="upload-label" htmlFor="fileInput">
              <div className="card">
                <img src={'http://45.9.25.190:8000' + imageURL} alt="" style={{ width: '50%' }} />
                <img src={'http://45.9.25.190:8000' + result} alt="" style={{ width: '50%' }} />
              </div>
            </label>
          </div>

      </div>
      <div className="button_load">
      <input className="up" type="file" id="fileInput" accept="image/*" onChange={handleFileChange} />
      <p className="upload-text">Выберите файл и загрузите</p>
      <button className="upload-button" onClick={handleUpload}>
        Загрузить
      </button>

</div>
<input className="rstplink" placeholder={"Вставьте вашу rtsp ссылку"} />



      {/* New section for output images */}
     <div className="output-images-container">
  <h2>Изображения с выделением оружия:</h2>
  {outputImages
    .filter((imageUrl) => imageUrl.includes('11.jpg') || imageUrl.includes('33.jpg') || imageUrl.includes('42.jpg') )
    .map((imageUrl, index) => (
      <img key={index} src={`http://45.9.25.190:8000${imageUrl}`} alt={`Output Image ${index}`} style={{ width: '300px', margin: '5px' }} />
    ))}
     </div>



      <div className="footer" style={{ backgroundColor: "#2474F6", width: "100%", color: "white", padding: "130px", textAlign: "center" }}>
      </div>
    </div>
  );
}

export default App;