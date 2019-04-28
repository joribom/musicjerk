import React, { Component } from 'react';
import { Redirect } from 'react-router-dom'
import PropTypes from 'prop-types';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import CreateIcon from '@material-ui/icons/Create';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import CircularProgress from '@material-ui/core/CircularProgress';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import withStyles from '@material-ui/core/styles/withStyles';
import authenticator from './Authenticator';

const lightTheme = createMuiTheme({
    palette: {
        primary: {
            main: '#ffffff',
        },
        secondary: {
            main: '#3f51b5'
        }
    },
})

const styles = theme => ({
  main: {
    width: 'auto',
    display: 'block', // Fix IE 11 issue.
    color: '#26262b',
    backgroundColor: '#26262b',
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(800 + theme.spacing.unit * 3 * 2)]: {
      width: 800,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing.unit * 8,
    backgroundColor: '#333',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
  },
  avatar: {
    margin: theme.spacing.unit,
    backgroundColor: '#3f51b5',
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing.unit,
  },
  submit: {
    marginTop: theme.spacing.unit * 3,
  },
  input: {
    color: '#ffffff',
    textColor: '#ffffff',
  },
  underline: {
    borderBottom: '1px solid white',
  }
});

class NewAlbum extends Component {

  constructor(props) {
    super(props);
    this.onSubmit = this.onSubmit.bind(this);
    authenticator.addStatusListener(this.forceUpdate, this);
    this.state = {
      suggested: false,
      accepted: false,
      canceled: false,
      title: '',
      artist: '',
      spotify_id: null,
      image_url: null,
    };
    this.spotifySearch = this.spotifySearch.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  onSubmit(event){
    event.preventDefault();
    const data = new FormData(event.target);
    authenticator.signIn(data);
  }

  spotifySearch(){
    const input = {
      title: this.state.title,
      artist: this.state.artist
    };
    fetch('/api/spotify_search', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    }).then(response => {
      response.json().then(data => {
        const spotify_id = data['spotify_id'];
        const image_url = data['image_url'];
        if (spotify_id != null){
          this.setState((state, props) => {
            return {
              suggested: true,
              accepted: false,
              canceled: false,
              spotify_id: spotify_id,
              image_url: image_url,
            };
          });
        }
      })
    })
  }

  render(){
    const { classes } = this.props;

    if (!authenticator.checked()){
      // If authenticator hasn't checked yet, wait for it.
      return <CircularProgress size='200' />
    } else if (!authenticator.validated()){
      // If user is not logged in, don't allow them to enter data.
      return <h1 style={{textAlign:'center'}}>Not signed in</h1>
    }

    return (
      <div className={classes.main}>
        <MuiThemeProvider theme={lightTheme}>
        <Paper className={classes.paper}>
          <Avatar className={classes.avatar}>
            <CreateIcon />
          </Avatar>
          <Typography className={classes.input} component="h1" variant="h5">
            Add new album
          </Typography>
          <form className={classes.form} onSubmit={this.onSubmit}>
            <div style={{display:'flex'}}>
              <div style={{width:'50%'}}>
                <FormControl margin="normal" style={{width: '100%'}}>
                  <InputLabel className={classes.input} htmlFor="title">Album title</InputLabel>
                  <Input className={classes.input} classes={{underline: classes.underline}} onChange={this.handleChange} ref={this.title} id="title" name="title" autoComplete="title" autoFocus />
                </FormControl>
                <br/>
                <FormControl margin="normal" style={{width: '100%'}}>
                  <InputLabel className={classes.input} htmlFor="artist">Artist</InputLabel>
                  <Input className={classes.input} classes={{underline: classes.underline}} onChange={this.handleChange} ref={this.artist} name="artist" type="artist" id="artist" autoComplete="artist" />
                </FormControl>
                <br/>
                <Button
                  variant="contained"
                  color="secondary"
                  className={classes.submit}
                  onClick={this.spotifySearch}
                >
                  Search on Spotify
                </Button>
                <br/>
                <FormControl margin="normal" style={{width: '100%'}}>
                  <InputLabel className={classes.input} htmlFor="title">Spotify id</InputLabel>
                  <Input className={classes.input} classes={{underline: classes.underline}} id="spotifyid" name="spotifyid" autoComplete="spotifyid" autoFocus />
                </FormControl>
                <br/>
                <FormControl margin="normal" style={{width: '100%'}}>
                  <InputLabel className={classes.input} htmlFor="artist">Image url</InputLabel>
                  <Input className={classes.input} classes={{underline: classes.underline}} name="imageurl" type="imageurl" id="imageurl" autoComplete="imageurl" />
                </FormControl>
                <br/>
              </div>
              {this.state.suggested && !this.state.accepted && !this.state.canceled &&
                <div style={{width:'50%', display:'flex', flexDirection:'column', alignItems:'center'}}>
                  <h2 className={classes.input}>Is this your album?</h2>
                  <br/>
                  <img src={this.state.image_url} style={{width:'75%', height:'75%'}}/>
                  <div style={{display:'flex', width:'100%'}}>
                    <div style={{width:'50%', display:'flex', justifyContent:'center'}}>
                      <Button
                        variant="contained"
                        color="secondary"
                        className={classes.submit}
                        style={{width:'70%'}}
                      >
                        Accept
                      </Button>
                    </div>
                    <div style={{width:'50%', display:'flex', justifyContent:'center'}}>
                      <Button
                        variant="contained"
                        color="secondary"
                        className={classes.submit}
                        style={{width:'70%'}}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                </div>
              }
            </div>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="secondary"
              className={classes.submit}
            >
              Add album
            </Button>
          </form>
        </Paper>
        </MuiThemeProvider>
      </div>
    );
  }
}

export default withStyles(styles)(NewAlbum);
