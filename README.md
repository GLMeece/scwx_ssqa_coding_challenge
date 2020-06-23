# Secureworks Software Quality Assurance/Automation Engineer Coding Challenge

The following README is intended to provide explanation and orientation to the coding challenge response for the [Senior Software Quality Assurance/Automation Engineer – Secureworks – Remote](https://jobs.dell.com/job/atlanta/senior-software-quality-assurance-automation-engineer-secureworks-remote/375/16267885) position. Questions/comments may be [directed to the author (Greg Meece)](mailto:glmeece@gmail.com?subject=SCWX%20Challenge).

## Original Instructions

The original instructions are located in [this document](original_instructions.md). Under the [**Design Thoughts** section](#design-thoughts) below, read about original design ideas, discarded paths, etc.

## Setup Instructions

Although it is highly likely that the test challenge code will run on similar OS versions, the author cannot guarantee beyond what is stated here. Although using a Docker container for the Linux endpoint was considered, because Docker containers for Windows tends to be problematic, using a VM for both platforms was chosen instead.

This challenge was developed and tested on:

* Windows 10 Student Edition, version 1903 (Virtual Machine)
* Ubuntu Linux 20.04 LTS (Virtual Machine)

In order to run the test against these endpoints, Python 3.8 should installed.  In the case of Ubuntu 20.04, Python 3.8 is already installed. Windows 10 will need to have it [installed by the user](https://www.python.org/).

Additionally, it is recommended that `pip` be upgraded:

### Ubuntu 20.04

```bash
sudo apt update
sudo apt install python3-pip
sudo apt install python-is-python3
```

### Windows

```powershell
# Running as Admin
python -m pip install --upgrade pip
```

To remove as much complexity as possible:

1. [Pull down the master branch as a Zip file](https://github.com/GLMeece/scwx_ssqa_coding_challenge/archive/master.zip) 
2. Unzip the archive.
3. CD into the directory for execution.
4. Using a terminal, execute: `pip3 -r requirements.txt` 
   Note that ideally one would have created a virtual environment for this execution, but that is left to the reader for brevity's sake.

## Execution

1. Using a terminal, run either the Windows Batch file (`run_tests_windows.bat`) or Linux Shell script (`run_tests_linux.sh`) to run the tests and create the test report and log.
2. To view the test results, open the `report.html` file in the `reports` directory. Additionally, you may wish to examine the `scwx_rc_test.log` log file in the same directory.

# Test Cases

## TestSensorReturn class

## `TestSensorReturn` class

Testing what is returned by sensor.

* `test_has_name`
    Verify process name is returned

* `test_has_pid`
    Verify PID is valid integer

* `test_pid_nonzero`
    Verify returned PID is > 0

* `test_status_running`
    Verify process is actually running

* `test_proc_is_malware`
    Looking for valid malware process

* `test_proc_is_not_malware`
    Verifying *not* malware process


## `TestDatabaseWrites` class

Does DB reflect what is expected?

* `test_values_written_in_db`
    Verifies that a proc record written to the database aligns with what 'Red Shawl' is reporting.
    Normally, this functionality would be within the connection class...


# Design Thoughts

To butcher _Robert Burns'_ poem
> The best laid schemes o' **Meece** an' men...

As I originally parsed the problem domain much too expansively. Due to this (and post-op medicine), I originally envisioned:

* Leverage existing processes on the host endpoint, leveraging the Python library [**psutil**](https://github.com/giampaolo/psutil#quick-links), provides cross-platform access to processes running on the host machine. 
  _Issues with this_: Lack of determinancy and a non-closed system eliminated this design approach. I expended nearly a day on this effort.
* As with above, add some additional "fake" processes to the mix in _N_ second intervals. The thought was to assign those processes names that will be used in testing so we can verify we see them emerge.
  _Issues with this_: This turns out to be problematic unless there are a lot of encapsulated executables ready for deployment. I.e., actually naming a new process is very platform specific (not to mention time-consuming), and the charter was to make this run on Windows and Linux. Mixed with the point above, added another several hours.
* The main language used is **Python** as it is the most familiar to the author, as well as being one of the more popular languages on the market now. Hence, it should be understandable by a larger audience than a less popular or more arcane language. Additionally, since it is largely cross-platform, this language choice should be usable/deployable for both Windows and Linux endpoints. I stuck with this language choice.
* The test harness used is [**PyTest**](https://docs.pytest.org/en/latest/) although I did not leverage all it is capable of doing (e.g., fixtures, mocks, etc.) Regardless, it's a powerful and robust harness that provides more functionality out of the box than UnitTest (a Python built-in) does. I did at the [**pytest-html** plugin](https://github.com/pytest-dev/pytest-html#pytest-html) for reporting convenience.
* I also explored using true Mocks, but even this effort proved too time-consuming and I opted instead for a small stub class that stands in for the endpoint and communication with it.
* Ultimately, the actual test cases are truncated and not nearly as comprehensive as would be the case if the existing ecosystem (e.g., something resembling _Red Cloak_) were in place to begin with. :frowning_face:
* I did endeavor to remain Python idiomatic, and leveraged [**Flake8**](https://flake8.pycqa.org/en/latest/index.html#) for linting and [**YAPF**](https://github.com/google/yapf#yapf) for formatting assistance.
