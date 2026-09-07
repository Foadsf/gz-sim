import sys
import yaml
import os
import argparse

def check(workflow_files):
    valid_job_found = False
    for wf in workflow_files:
        if not os.path.exists(wf):
            continue
        with open(wf) as f:
            data = yaml.safe_load(f)

        jobs = data.get('jobs', {})
        for job_name, job in jobs.items():
            found_testing = False
            found_ctest = False
            steps = job.get('steps', [])
            for step in steps:
                run_cmd = step.get('run', '')
                if 'BUILD_TESTING=ON' in run_cmd:
                    found_testing = True
                if 'ctest' in run_cmd:
                    found_ctest = True

            if found_testing and found_ctest:
                print(f"PASS: Found valid job '{job_name}' in '{wf}' with BUILD_TESTING=ON and ctest.")
                valid_job_found = True
                break
        if valid_job_found:
            break

    if not valid_job_found:
        print("FAIL: Could not find a job with both BUILD_TESTING=ON and ctest.")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', default=['.github/workflows/windows-test.yml', '.github/workflows/windows-ci.yml'])
    args = parser.parse_args()
    check(args.files)
