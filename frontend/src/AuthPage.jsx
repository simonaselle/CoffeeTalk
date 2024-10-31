import axios from "axios";

const AuthPage = (props) => {
    const onSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        axios.post(
            'http://localhost:8000/authenticate',
            { username, password }
        ).then(() => {
            props.onAuth({ username, secret: password });
        }).catch((error) => {
            console.error("Authentication failed:", error);
        });
    }

    return (
        <div className="background">
            <style>
                {`
                .auth-input::placeholder,
                .auth-password::placeholder {
                    color: rgb(175, 175, 175); /* Placeholder text color */
                    font-family: Avenir; /* Placeholder text font */
                }
                `}
            </style>
            <form onSubmit={onSubmit} className="form-card">
                <div className="form-title">
                    Welcome To Coffeetalk ☕
                </div>

                <div className="form-subtitle">
                    Set a username and password to begin
                </div>

                <div className="auth">
                    <input className="auth-input" name="username" placeholder="Username" />
                    <input className="auth-password" name="password" type ="password" id="password" placeholder="Password" />
                    <button className="auth-button" type="submit">Enter</button>
                    <button className="about-button" type="creators">About Creators</button>
                </div>
            </form>
        </div>
    );
}

export default AuthPage