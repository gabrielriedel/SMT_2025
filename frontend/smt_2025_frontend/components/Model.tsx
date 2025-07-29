// 'use client'
// import React, { useState, useEffect } from 'react';
// import { Button } from '@/components/ui/button';

// interface FormData {
//   pitcher_hand: number;
//   batter_hand: number;
//   pitchOfPA: number;
//   paOfInning: number;
//   pitch: string;
//   pitchLocation: number;
//   wave: string;
// }

// const options = {
//   pitcher: ['Bueno, Reece', 'Cooper, Troy', 'Downs, Chris', 'Hoiland, Cam', 'Kalfsbeek, Luke', 'Kvidahl, Erik', 'Marmie, Ethan', 'Montgomery, Paul','Morano, Josh', 'Naess, Griffin', 'Pearlman, Caden','Royle, Charlie', 'Sagouspe, Tanner', 'Souza, Henry','Torres, Jaccob', 'Volmerding, Joshua'],
//   inning: Array.from({ length: 9 }, (_, i) => i + 1),
//   pitchOfPA: Array.from({ length: 30 }, (_, i) => i + 1),
//   paOfInning: Array.from({ length: 30 }, (_, i) => i + 1),
//   pitch: ['Fastball', 'Slider', 'Changeup', 'Curveball', 'Sinker', 'Splitter', 'Cutter'],
//   pitchLocation: Array.from({ length: 6 }, (_, i) => i + 1),
//   wave: ['None', 'Wave', 'Extreme Wave']
// };

// export default function Home() {
//   const [formData, setFormData] = useState<FormData>({
//     pitcher: '', inning: 0, pitchOfPA: 0, paOfInning: 0, pitch: '', pitchLocation: 0, wave: ''
//   });

//   const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
//     const { name, value } = e.target;
//     setFormData((prev) => ({ ...prev, [name]: value }));
//   };

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     try {
//       const response = await fetch('/api/createActivity', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           pitcher_name: formData.pitcher,
//           inning: formData.inning,
//           pitch_of_pa: formData.pitchOfPA,
//           pa_of_inning: formData.paOfInning,
//           exp_pitch: formData.pitch,
//           exp_location: formData.pitchLocation,
//           wave: formData.wave
//         })
//       });
//       const result = await response.json();
//       console.log('API Response:', result);
//       alert('Submission successful!');
//     } catch (error) {
//       console.error('Submission error:', error);
//       alert('Failed to submit. Check the console for details.');
//     }
//   };

//   return (
//     <main className="flex-1 flex flex-col gap-6 px-4">
//       <h2 className="font-medium text-xl mb-4">Pitch Location Entry</h2>
//       <form className="grid grid-cols-2 gap-4" onSubmit={handleSubmit}>
//         <div className="grid grid-cols-1 gap-4">
//           {(['pitcher', 'inning', 'pitchOfPA', 'paOfInning'] as Array<keyof FormData>).map((key) => (
//             <div key={key} className="flex flex-col">
//               <label className="font-medium capitalize" htmlFor={key}>{key}</label>
//               <select id={key} name={key} value={formData[key]} onChange={handleChange} className="border rounded p-2" required>
//                 <option value="">Select {key}</option>
//                 {options[key].map((option, index) => (
//                   <option key={index} value={option}>{option}</option>
//                 ))}
//               </select>
//             </div>
//           ))}
//         </div>
//         <div className="grid grid-cols-1 gap-4">
//           {(['pitch', 'pitchLocation', 'wave'] as Array<keyof FormData>).map((key) => (
//             <div key={key} className="flex flex-col">
//               <label className="font-medium capitalize" htmlFor={key}>{key}</label>
//               <select id={key} name={key} value={formData[key]} onChange={handleChange} className="border rounded p-2" required>
//                 <option value="">Select {key}</option>
//                 {options[key].map((option, index) => (
//                   <option key={index} value={option}>{option}</option>
//                 ))}
//               </select>
//             </div>
//           ))}
//         </div>
//         <div className="col-span-2 flex justify-center mt-4">
//           <Button type="submit">Submit</Button>
//         </div>
//       </form>
//     </main>
//   );
// }
