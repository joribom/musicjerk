import Cookies from 'js-cookie';

class Authenticator {
  constructor(){
    this._username = null;
    this.uid = null;
    this.session = null;
    this._validated = false;
    this._checked = false;
    this.eventHandlers = [];
    this.eventObjects = [];
    this.validate();
  }

  validate(){
    const username = Cookies.get('username');
    const uid = Cookies.get('uid');
    const session = Cookies.get('session');
    const input = {
      uid: uid,
      session: session,
    };
    fetch('/api/validate', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    }).then(response => {
      response.json().then(data => {
        if (data['authenticated']){
          this._username = username;
          this.uid = uid;
          this.session = session;
          this._validated = true;
        }
        this._checked = true;
        this.statusChanged();
      })
    })
  }

  addStatusListener(handler, obj){
    this.eventHandlers.push(handler);
    this.eventObjects.push(obj);
  }

  statusChanged(){
    for (var i = 0; i < this.eventHandlers.length; i++){
      const handler = this.eventHandlers[i];
      const object = this.eventObjects[i];
      handler.call(object);
    }
  }

  validated(){
    return this._validated;
  }

  checked(){
    return this._checked;
  }

  username(){
    return this._username;
  }

  signIn(formData){
    fetch('/api/login', {
      method: 'POST',
      body: formData,
    }).then(response => {
      response.json().then(data => {
        if (data['auth']){
          this.uid = data['data']['uid'];
          this.session = data['data']['session'];
          this._username = data['data']['username'];
          this._validated = true;
          this.updateCookies();
          this.statusChanged();
        }
      })
    });
  }

  signOut() {
    this._username = null;
    this.uid = null;
    this.session = null;
    this._validated = false;
    this.updateCookies();
    this.statusChanged();
  }

  updateCookies(){
    Cookies.set('uid', this.uid, { path: '/' });
    Cookies.set('session', this.session, { path: '/' });
    Cookies.set('username', this._username, { path: '/' });
  }
}

const authenticator = new Authenticator();

export default authenticator;
