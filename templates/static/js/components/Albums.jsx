import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import CircularProgress from '@material-ui/core/CircularProgress';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import CameraIcon from '@material-ui/icons/PhotoCamera';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { withStyles } from '@material-ui/core/styles';


const darkTheme = createMuiTheme({
    typography: {
      color: 'white',
    },
    palette: {
        type: 'dark',
        primary: {
            main: '#26262b',
            textColor: '#ffffff',
            background: '#26262b',
        },
        secondary: {
            main: '#3f51b5',
        },
        textPrimary: '#ffffff'
    },
})

const styles = theme => ({
  appBar: {
    position: 'relative',
  },
  icon: {
    marginRight: theme.spacing.unit * 2,
  },
  heroUnit: {
    backgroundColor: '#26262b',
    textColor: '#ffffff'
  },
  heroContent: {
    maxWidth: 600,
    margin: '0 auto',
    padding: `${theme.spacing.unit * 8}px 0 ${theme.spacing.unit * 6}px`,
  },
  heroButtons: {
    marginTop: theme.spacing.unit * 4,
  },
  layout: {
    width: 'auto',
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(1100 + theme.spacing.unit * 3 * 2)]: {
      width: 1100,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  cardGrid: {
    padding: `${theme.spacing.unit * 8}px 0`,
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  cardMedia: {
    paddingTop: '56.25%', // 16:9
  },
  cardContent: {
    flexGrow: 1,
  },
  footer: {
    backgroundColor: '#26262b',
    padding: theme.spacing.unit * 6,
  },
  h2: {
    textColor: '#ffffff',
  }
});

class Albums extends Component {

    constructor(props){
        super(props);
        this.classes = props.classes;
        this.state = {
            albums: [],
            loading: true,
        };
    }

    componentDidMount(){
        fetch('/api/album-averages', {
          method: 'GET'
        }).then(response => response.json()
        .then(data => {
          this.setState((state, props) => {
            return {albums: data, loading: false};
          });
        }));
    }

  render(){
  const { albums } = this.state;
  return (
    <React.Fragment>
      <MuiThemeProvider theme={darkTheme}>
      <main>
        {/* Hero unit */}
        <div className={this.classes.heroUnit}>
          <div className={this.classes.heroContent}>
            <Typography component="h1" variant="h2" align="center" color="textPrimary" classes={{h2: this.classes.h2}} gutterBottom>
              Previous Albums
            </Typography>
            <Typography variant="h6" align="center" color="textSecondary" paragraph>
              These are all the albums that have been chosen for Musicjerk.
            </Typography>
            <div className={this.classes.heroButtons}>
            </div>
          </div>
        </div>
        <div className={classNames(this.classes.layout, this.classes.cardGrid)}>
          {/* End hero unit */}
          <Grid container spacing={40}>
            {albums.map(album => (
              <Grid item key={album.title} sm={6} md={4} lg={3}>
                <Card className={this.classes.card}>
                  <CardMedia
                    className={this.classes.cardMedia}
                    image={album.image_url != null ? album.image_url : 'https://cidco-smartcity.niua.org/wp-content/uploads/2017/08/No-image-found.jpg'}
                    title={album.title}
                  />
                  <CardContent className={this.classes.cardContent}>
                    <Typography gutterBottom variant="h5" component="h2">
                      {album.title}
                    </Typography>
                    <Typography>
                      {album.summary.length > 100
                        ? (album.summary.substring(0,97) + '...')
                        : album.summary}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" variant="contained" color="secondary"
                    component={NavLink} to={'/albums/' + album.url}>
                      View
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </div>
      </main>
      {/* Footer */}
      <footer className={this.classes.footer}>
        <Typography variant="h6" align="center" gutterBottom>
          Big Musicjerk
        </Typography>
        <Typography variant="subtitle1" align="center" color="textSecondary" component="p">
          That's all folks!
        </Typography>
      </footer>
      {/* End footer */}
      </MuiThemeProvider>
    </React.Fragment>
  );
  }
  }

Albums.propTypes = {
  classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(Albums);
