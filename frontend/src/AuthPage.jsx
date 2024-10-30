import axios from "axios";

const AuthPage = (props) => {
    const onSubmit = (e) => {
        e.preventDefault();
        const { value } = e.target[0];
        axios.post(
            'http://localhost:3001/authenticate',
            { username: value }
        )
        props.onAuth({ username: value, secret: value })
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