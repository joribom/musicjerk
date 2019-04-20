import Cookies from 'js-cookie';

class Authenticator {
  constructor(){
    this.username = null;
    this.uid = null;
    this.session = null;
    this._validated = false;
    this._checked = false;
    this.validate();
  }

  async validate(){
    const username = Cookies.get('username');
    const uid = Cookies.get('uid');
    const session = Cookies.get('session');
    const input = {
      uid: 2,
      session: 'hK5Wjthwil_wrOk6SIhaTg',
    };
    const response = await fetch('/api/validate', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    });
    const data = await response.json();
    console.log("Got response!");
    if (data['authenticated']){
        this.username = username;
        this.uid = uid;
        this.session = session;
        this._validated = true;
        console.log("Validated!")
    };
  }

  async validated(){
      if (!this._checked){
          await this.validate();
      }
      return this._validated;
  }

  signIn(username, password){

  }

  signOut() {
    // clear id token, profile, and expiration
    this.username = null;
    this.uid = null;
    this.session = null;
  }
}

const authenticator = new Authenticator();

export default authenticator;
