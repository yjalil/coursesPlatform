import React, { useEffect } from 'react';
import './App.css';



function App() {
  const [rerender, setRerender] = React.useState(false);
  const [userData, setUserData] = React.useState({});
  const GITHUB_CLIENT_ID = 'Ov23liKeBgl8TdECQjjQ';
  // const GITHUB_CLIENT_SECRET = '653b8ec4bbcd8a2d5cb37758c8732592bbfebf68';
  const githubOAuthURL = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&scope=user`;

  React.useEffect(() => {
      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);
      const code = urlParams.get('code');
      console.log(code);
      if (code && (localStorage.getItem('accessToken') === null)) {
        async function getAccessToken(code) {
            await fetch('http://localhost:8000/access_token?code='+code, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((response) => response.json())
            .then((data) => {
              console.log(data);
              if (data.access_token) {
                localStorage.setItem('accessToken', data.access_token);
                setRerender(!rerender);
              }
          })
        }
          getAccessToken(code);

}
}, []);

async function getUserData() {
  const token = localStorage.getItem('accessToken');
  const requestOptions = {
      method: 'GET',
      headers: {
          'Authorization': `Bearer ${token}`
      }
  };

  await fetch('http://localhost:8000/user', requestOptions)
      .then((response) => response.json())
      .then((data) => {
          console.log(data);
          setUserData(data);
      })
      .catch((error) => {
          console.error('Error:', error);
      });
}


  function GitLogin() {
    window.location.assign(githubOAuthURL);
   }

   function LogOut() {
    localStorage.removeItem('accessToken');
    setRerender(!rerender);
   }

  return (
    <div className="App">
        <h1>GitHub OAuth with React</h1>

        {localStorage.getItem('accessToken') ? (
    <>
        <button onClick={getUserData}>Get User Data</button>
        <button onClick={LogOut}>Logout</button>
        {console.log(Object.keys(userData).length)}
    </>
) : (
    <button onClick={GitLogin}>Login with GitHub</button>
)}
      </div>
  );
}

export default App;
