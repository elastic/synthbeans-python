# SynthBean

## Overview

SynthBean is one of the family of Elastic Opbeans but instead of instrumenting a real application,
such as Django or Flask, it instruments a specially-designed "pseudo-application" which is purpose-built
specifically to provide certain values to the agent.

This SynthBean is built using the APM Python Agent for its instrumentation.

## Why SynthBean?

This project may be useful if you have one or more of the following needs:

* You wish to quickly and easily create some APM data and you do not care much what the data is.
* You wish to quickly and easily create some APM data and you _do care_ that the spans are exactly consistent. (i.e., a span is always exactly the same duration). This may be helpful if want to see the how the APM application behaves when there is no variation between values and may be a good way to verify that certain calculations are being performed correctly.
* You wish to spin up a large number of "instances" in the APM application and you do not care what data is produced.

## Examples

<img width="1604" alt="Capture d’écran 2021-03-15 à 10 50 58" src="https://user-images.githubusercontent.com/111616/111137985-53e43800-8577-11eb-826b-baeddd2d1681.png">

SynthBean producing two spans at 1s and 5s



## Installation and Running 

The project uses Poetry as its build and dependency manger. You can install the requirements
by running: `poetry install` from the project root. If you do not have Poetry installed, you must
first do so, probably by running `pip install poetry`. 

After the dependencies are installed, you may run the application with `poetry run python synthbean.py`. 

Of course, if you are familiar with Python and have a preferred method of managing dependencies, you are free to use whatever tool you like. All dependencies are defined in `pyproject.toml`.

## Configuration

Configuration is split into two separate files. The first defines a configuration for the APM Agent
and the second defines the type of synthetic data you wish the application to send.

### Configuring the Agent

Configure the agent by editing `conf/settings.ini`. Settings which are listed there are the only settings
which will be included. Any additional settings added to the file will be ignored.

You may also configure SynthBean through the use of environment variables. Below is a list of variables
which may be set in the environment and the variables that they control in the application:

|Environment variable|Application variable|Description|
|--------------------|--------------------|-----------|
|SYNTHBEAN_SERVER_URL|server_url|The URL of the Elasticsearch server to connect to|
|SYNTHBEAN_SERVICE_NAME|service_name|The service name of the Synthbean|
|SYNTHBEAN_ENVIRONMENT|environment|The application environment in APM|
|SYNTHBEAN_CLOUD_PROVIDER|cloud_provider|The cloud provider value in APM|

### Configuring the Application

The application is controlled by editing `conf/synthbean.yml`.

#### Spans

The SynthBean configuration file contains a top-level key called `spans`. The value of this key are dictionaries
where each key is the name of a span and the value is configuration for that span. The only configuration currently
supported is `duration` which is specified in milliseconds.

Example:

```
spans:
  first_span:
    duration: 1000
  second_span:
    duration: 5000
```
The above specifies two spans. The first span is named `first_span` and has a duration of 1s. The second span, unsurprisingly,
is named `second_span` and has a duration of 5s.

#### Smoothing Strategies

The application will attempt to schedule the first span at 1s intervals and the second span at 5s intervals. Because there is a small
amount of overhead (typically ~1ms), the duration values will be corrected before being sent to the APM server. For example, a span
which takes 1,002ms to run will be corrected to 1,000ms prior to being sent.

Take careful note that applying the `floor` smoother means that target span values of 1,000 and 1,500 will both be rounded down to 1,000! Sub-second smoothing is not currently available.

The following strategies for smoothing are currently supported:

|Name|Description|
|---------|----------|
|floor|Rounds downward to the nearest whole second|
|null|No smoothing is applied. Actual values will be sent.|

#### Instance Spoofing

SynthBean also supports spoofing "instance spoofing" and making it appear as if requests for the single SynthBean application are
originating from many containers. SynthBean will still attempt to schedule spans exactly as it would otherwise, but it will use
n-number of APM clients to do so.

You will see instances appear with the `synthbean-python-<n>` prefix, starting from the number 1.

This can be used as a quick way to see what it looks like when you connect a large number of instances to the APM application. A single
SynthBean can easily scale into the thousands of instances and provide throughput in excess of 100,000 tpm. 

To enable Instance Spoofing, set `instance_count` in the SynthBean configuration to the number of
instances you would like to spoof.

Note that at least three threads will be allocated for every instance and some machines may experience thread exhaustion beyond 500 instances.

#### Jitter

Spans can introduce jitter which will vary the amount of delay by a specified number of milliseconds. For each span which is sent, a random number
is chosen between 0 and the number specified in the span configuration. The number is then either added or subtracted from the goal span length pseudo-randomly. 

Note: If any span has a `jitter` configuration set, you must not use any smoothing strategy. Attempting to use jitter with smoothing will result
in an error and the application will exit.

Example:

```
jitter: 1
  duration:
    first_span:
    duration: 1000
    jitter: 10
```

The above will result in duration values between 990 an 1010.

#### Named Instances

If you wish, you may name instances and give them individual span profiles:

```
instances:
  fast_instance:
    spans:
      instance_based_first_span:
        duration: 2000
      instance_based_second_span:
        duration: 2000
  slow_instance:
    spans:
      instance_based_first_span:
        duration: 3000
      instance_based_second_span:
        duration: 3000
````


#### Caveats

The `floor` smoother always rounds _down_ to the nearest second. Therefore, you should always choose values of no less than
1,000! If you choose a value below 1,000, the value sent to the APM server will be zero.