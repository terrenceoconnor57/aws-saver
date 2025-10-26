terraform {
  cloud {
    organization = "aws-saver"

    workspaces {
      name = "aws-saver-dev"
    }
  }
}

