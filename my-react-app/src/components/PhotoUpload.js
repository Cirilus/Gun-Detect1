// PhotoUpload.js
import React, { useState } from 'react';
import axios from 'axios';

function PhotoUpload({ setUploadedPhotoURL }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const imageURL = response.data.image_url;
      setUploadedPhotoURL(imageURL);
      setSelectedFile(null);
    } catch (error) {
      console.error('Ошибка при загрузке изображения', error);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Загрузить фото</button>
    </div>
  );
}

export default PhotoUpload;
