# calconnect

## Deployment:
Automated CI/CD pipelines have been set up using Amazon CodeCommit, CodePipeline, and Elastic Beanstalk.

A push to master will automatically update the calconnect-prod server.  These changes will be reflected at this url: [http://calconnect.us-east-1.elasticbeanstalk.com/](http://calconnect.us-east-1.elasticbeanstalk.com/)

A push to dev will automatically update the calconnect-dev server.  These changes will be reflected at this url: [http://calconnect-dev.us-east-1.elasticbeanstalk.com/](http://calconnect-dev.us-east-1.elasticbeanstalk.com/)