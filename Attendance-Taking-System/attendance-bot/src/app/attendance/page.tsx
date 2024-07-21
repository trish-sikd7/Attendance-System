"use client"
import { useEffect, useState } from "react";
import Image from "next/image";

export default function Example() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    async function fetchStudentAttendance() {
      try {
        const response = await fetch("http://127.0.0.1:8000/student_attendance");
        const data = await response.json();
        setStudents(data);
      } catch (error) {
        console.error("Error fetching student attendance:", error);
      }
    }

    fetchStudentAttendance();
  }, []);

  return (
    <div className="bg-white">
      <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
        <h2 className="sr-only">Products</h2>

        <div className="grid grid-cols-1 gap-y-4 sm:grid-cols-2 sm:gap-x-6 sm:gap-y-10 lg:grid-cols-3 lg:gap-x-8">
          {students.map((student) => (
            <div
              key={student.image_id}
              className="group relative flex flex-col overflow-hidden rounded-lg border border-gray-200 bg-white"
            >
              <div className="aspect-h-4 aspect-w-3 bg-gray-200 sm:aspect-none group-hover:opacity-75">
                <Image
                  src={`data:image/png;base64,${student.image_data}`}
                  alt={student.name}
                  className="h-full w-full object-cover object-center sm:h-full sm:w-full"
                  width={640}
                  height={480}
                />
              </div>
              <div className="flex flex-1 flex-col space-y-2 p-4">
                <h3 className="text-sm font-medium text-gray-900">
                  {student.name}
                </h3>
                <p className="text-sm text-gray-500">
                  {`${student.roll_no} - ${student.department} - ${student.year}`}
                </p>
                <div className="flex flex-1 flex-col justify-end">
                  <p className="text-sm italic text-gray-500">
                    {student.email}
                  </p>
                  <p className="text-base font-medium text-gray-900">
                    {student.phone}
                  </p>
                  <p className="text-base font-medium text-green-400">
                    {student.timestamp}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
