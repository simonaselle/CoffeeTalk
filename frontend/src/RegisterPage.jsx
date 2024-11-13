// import React from 'react';

// const RegisterPage = () => {
//     const onSubmit = (e) => {
//         e.preventDefault();
//         const username = e.target.username.value;
//         const password = e.target.password.value;
//         // Add your registration logic here
//         console.log('Registering new user:', username, password);
//     }

//     return (
//         <div className="background">
//             <div className="form-card">
//                 <h1 className="main-heading">Register</h1>
//                 <form onSubmit={onSubmit}>
//                     <div className="form-subtitle">
//                         Create a new account
//                     </div>

//                     <div className="auth">
//                         <input className="auth-input" name="username" placeholder="Username" />
//                         <input className="auth-password" name="password" type="password" placeholder="Password" />
//                         <button className="auth-button" type="submit">Register</button>
//                     </div>
//                 </form>
//             </div>
//         </div>
//     );
// }

// export default RegisterPage;