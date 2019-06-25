# Smoke test environment for indy clustering with auditquery

## Pre-requision
  * java  
  * git
  * mvn
  * docker 
  * docker-compose

## Notes
  * This project is using my owned repos of indy & auditquery with "changelog" branch, because currently these two project does not support ispn configuration overriding with customized ways. When this overriding is support in future, will switch to upstream git.

## Steps
  * Run prepare.sh: will download two projects and build, then use prepared docker build env to build docker file
  * Run docker-compose up in this root dir: will start these two built images
  * Access both localhost:8080 for indy and localhost:8082 for auditquery, and test repository change log features
  
