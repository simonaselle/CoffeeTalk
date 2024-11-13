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
            <div className="form-card">
                <h1 className="main-heading">Welcome to CoffeeTalk☕</h1>
                <form onSubmit={onSubmit}>
                    <div className="form-subtitle">
                        Set a Username and Password to get started.
                        New User? Click "New User" to create an account.
                    </div>

                    <div className="auth">
                        <input className="auth-input" name="username" placeholder="Username" />
                        <input className="auth-password" name="password" type="password" id="password" placeholder="Password" />
                        <button className="auth-button" type="submit">Enter</button>
                        <button className="new-user-button" type="button">New User</button>
                        <button className="about-button" type="button">About Creators</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default AuthPage;