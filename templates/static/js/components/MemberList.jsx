import React, { Component } from 'react';
import withStyles from '@material-ui/core/styles/withStyles';

const styles = theme => ({

    membersList: {
        marginLeft: '8px'
    }
});

class MemberList extends Component {

    constructor(props){
        super(props);
        this.classes = props.classes;
    }

    render () {
        const members = [];
        for (const index in this.props.members){
            const member = this.props.members[index];
            members.push(
              <li><a key={member.name} href={member.url}>{member.name}</a></li>
            );
        }
        return (
          <div>
            <h2>Our Members:</h2>

            <ol id="member_list" className={this.classes.membersList}>
              {members}
            </ol>
          </div>
        );
    }
}

export default withStyles(styles)(MemberList);
