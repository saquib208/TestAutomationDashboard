import xml.etree.ElementTree as ET
import re
import os

def extract_comment_1(testcase):
    result = {
        'TEST CASE ID': '',
        'TEST DESCRIPTION': '',
        'TESTED DIAGRAMS': '',
        'TESTED REQUIREMENTS': ''
    }

    # Iterate through the elements to find comment nodes (which may be in element text)
    for elem in testcase.iter():
        #print("--->",elem)
        if elem is not None and elem.tag is ET.Comment:
            comment_text = elem.text.strip()

            # Extract data from the comment using regular expressions
            test_case_id_match = re.search(r'TEST CASE ID:\s*(.*)', comment_text)
            test_description_match = re.search(r'TEST DESCRIPTION:\s*(.*?)(?=TESTED DIAGRAMS)', comment_text, re.DOTALL)
            tested_diagrams_match = re.search(r'TESTED DIAGRAMS:\s*(.*)', comment_text)
            tested_requirements_match = re.search(r'TESTED REQUIREMENTS:\s*(.*)', comment_text)

            if test_case_id_match:
                result['TEST CASE ID'] = test_case_id_match.group(1).strip()
            if test_description_match:
                result['TEST DESCRIPTION'] = test_description_match.group(1).strip()
            if tested_diagrams_match:
                result['TESTED DIAGRAMS'] = tested_diagrams_match.group(1).strip()
            if tested_requirements_match:
                result['TESTED REQUIREMENTS'] = tested_requirements_match.group(1).strip()

    #print(result)
    return result


# Helper function to determine the test case status
def determine_status(failures, errors, skipped):
    if skipped > 0:
        return 'skipped'
    elif failures > 0 or errors > 0:
        return 'fail'
    else:
        return 'pass'

def extract_failure_details(testcase):
    failure_elem = testcase.find('failure')

    if failure_elem is not None:
        #print("failure_elem", failure_elem.attrib)
        fail_dict= {
            'failure_message': failure_elem.attrib.get('message', ''),
            'failure_type': failure_elem.attrib.get('type', ''),
            'failure_details': failure_elem.text.strip() if failure_elem.text else 'No details available'
        }
        #print(fail_dict)
        return fail_dict
    return None


# Helper function to parse individual XML files
def parse_single_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract test suite attributes
    testsuite_name = root.attrib['name']
    total_tests = int(root.attrib['tests'])
    failures = int(root.attrib['failures'])
    #print("failures-->",failures)
    errors = int(root.attrib['errors'])
    skipped = int(root.attrib['skipped'])
    total_time = float(root.attrib['time'])

    # Extract test case details
    test_cases = []
    for testcase in root.findall('testcase'):

        failure_details = extract_failure_details(testcase)
        #print(failure_details)
        case = {
            'name': testcase.attrib['name'],
            'classname': testcase.attrib['classname'],
            'assertions': int(testcase.attrib['assertions']),
            'time': float(testcase.attrib['time']),
            'status': determine_status(failures, errors, skipped),
            'failure':failure_details
        }


        #Extract and parse comments for additional test details
        #comments = extract_comment_1(testcase)
        #case.update(comments)  # Add parsed comment details to the test case

        test_cases.append(case)

    total_result = {
        'testsuite_name': testsuite_name,
        'total_tests': total_tests,
        'failures': failures,
        'errors': errors,
        'skipped': skipped,
        'total_time': total_time,
        'test_cases': test_cases
    }
    return total_result

# Function to parse all XML files and aggregate the results
def parse_all_xml(directory_path):
    all_test_cases = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0

    # Loop through each XML file in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.xml'):
            file_path = os.path.join(directory_path, file_name)
            parsed_data = parse_single_xml(file_path)
            #print(parsed_data)

            # Aggregate the test results
            all_test_cases.extend(parsed_data['test_cases'])
            total_tests += parsed_data['total_tests']
            total_failures += parsed_data['failures']
            total_errors += parsed_data['errors']
            total_skipped += parsed_data['skipped']
            total_time += parsed_data['total_time']

    # Return the aggregated results
    aggregate_resut= {
        'total_tests': total_tests,
        'failures': total_failures,
        'errors': total_errors,
        'skipped': total_skipped,
        'total_time': round(total_time/60,3),
        'test_cases': all_test_cases
    }
    #print(aggregate_resut)
    return aggregate_resut

if __name__ == "__main__":
    # Example usage: parse all XML files in the 'data/' directory
    report_data = parse_all_xml('../data')
    #print(report_data)
