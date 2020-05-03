# Deep Deblurring Backend
This Flask API has two main objectives regarding Deep Deblurring Project:

1. Expose the predictions engine publicly in a secure and controlled way, through OAuth Protocols and Traffic Throttle Policies (Due to our budget limitations, we must set up very strict usage policies)
2. Collect user-generated training data and store it on a database. We will use this data to further improve the performance of the model during it lifecycle

On the next visualization, the block named "Flask API" represents this repository codebase, that interacts with almost every major component of Deep Deblurring System Architecture, so this is the central component that allows this service to exists

![Image](https://github.com/ElPapi42/deep-deblurring-serving/blob/master/SystemArchitecture.png "Arch")

This API will have two main consumers, our Web Application, and Third-party costumers that integrate our services with their applications.

PD: Deep Deblurring is not a Commercial Project, but a Student Project developed as a real-life Product Application to maximize learning.
