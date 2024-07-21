"use client"

import React, { useState } from 'react';

const CreateStudentForm = () => {
  const [studentData, setStudentData] = useState({
    image_id: '',
    name: '',
    department: '',
    year: '',
    roll_no: '',
    email: '',
    phone: '',
    image_data: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setStudentData({
      ...studentData,
      [name]: value,
    });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setStudentData({
        ...studentData,
        image_data: reader.result,
      });
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/create-student', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studentData),
      });

      if (response.ok) {
        console.log('Student created successfully');
        // Reset the form or redirect to another page
      } else {
        console.error('Failed to create student');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8 p-4 bg-white shadow-md rounded-md">
      <label className="block mb-4">
        <span className="text-gray-700">Image ID:</span>
        <input type="text" name="image_id" value={studentData.image_id} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Name:</span>
        <input type="text" name="name" value={studentData.name} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Department:</span>
        <input type="text" name="department" value={studentData.department} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Year:</span>
        <input type="text" name="year" value={studentData.year} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Roll No:</span>
        <input type="text" name="roll_no" value={studentData.roll_no} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Email:</span>
        <input type="text" name="email" value={studentData.email} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Phone:</span>
        <input type="text" name="phone" value={studentData.phone} onChange={handleInputChange} className="form-input mt-1 block w-full" />
      </label>
      <label className="block mb-4">
        <span className="text-gray-700">Image:</span>
        <input type="file" accept="image/*" onChange={handleImageChange} className="form-input mt-1 block w-full" />
      </label>
      <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600">
        Create Student
      </button>
    </form>
  );
};

export default CreateStudentForm;
