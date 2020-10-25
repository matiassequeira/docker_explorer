#!/usr/bin/env python3

import json
import re
import argparse
import os
import shutil

cwd= os.getcwd()
triaged_path= os.path.join(cwd, "triaged")

def triage_critical_file(in_file_name, out_file_name):
    if out_file_name is None:
        out_file_name= f'triaged_{in_file_name}'
    
    in_file= open(f'../{in_file_name}',"r")
    out_file= open(out_file_name,"w")
    discarded_elements_file= open(f'discarded_{in_file_name}',"w")
    critical_elements=list()
    private_keys=list()
    discarded_elements=list()
    for line in in_file.readlines():
        is_private_key=False
        discard=False
        try:
            line= json.loads(line)
            value= line.get('value')
            if is_example(line.get('file')): discard= True
            elif line.get('message') in ['Password']:
                if len(value) <= 10: discard= True
                 # At least a number and a letter
                elif not bool(re.match('^(?=.*[a-zA-Z])(?=.*[0-9])', value)): discard= True
                elif ' ' in value: discard= True
                elif 'PASSWORD' in value.upper(): discard= True
                elif value.upper().startswith('/USR/'): discard= True
                elif value.upper().startswith('INCLUDE/'): discard= True
                elif value.upper().startswith('/TMP/'): discard= True
                elif value.upper().startswith('/HOME'): discard= True
                elif value.upper()=='[WSO2CARBON]': discard= True
            elif line.get('message') == 'Private key':
                if len(value) < 300: discard= True
                if '>' in value or '<' in value or ':' in value: discard= True
                is_private_key=True
            elif line.get('message') == 'Private SSH key file':
                is_private_key=True
            
            if discard:
                discarded_elements.append(line)
                continue
            elif is_private_key:
                private_keys.append(line)
            else:
                critical_elements.append(line)
            
            store_triaged_file(line.get('file'))

        except Exception as e:
            print(f"Error triaging critical: {e}. Line: {line}\n")
    
    critical_elements= remove_duplicated_key_values(critical_elements)
    for i in critical_elements:
        out_file.write(json.dumps(i)+'\n')
    for i in private_keys:
        out_file.write(json.dumps(i)+'\n')
    for i in discarded_elements:
        discarded_elements_file.write(json.dumps(i)+'\n')

    in_file.close()
    out_file.close()
    discarded_elements_file.close()

def split_path_by_dir(path):
    path = os.path.normpath(path)
    return path.split(os.sep)

def store_triaged_file(entire_file_path):
    split_path = split_path_by_dir(entire_file_path)
    explorer_dir= split_path[2]
    file_name= split_path[-1]

    original_file_path = os.path.join(cwd, explorer_dir, file_name)
    copied_file_path = os.path.join(triaged_path, explorer_dir)
    
    # os.makedirs(os.path.dirname(copied_file_path), exist_ok=True)
    os.makedirs(copied_file_path, exist_ok=True)
    shutil.copy(original_file_path, copied_file_path)

def is_example(entire_file_path):
    path = os.path.normpath(entire_file_path)
    split_path = path.split(os.sep)
    file_name= split_path[-1]
    if 'EXAMPLE' in file_name.upper():
        return True
    else:
        return False

def triage_blocker_file(in_file_name, out_file_name):
    if out_file_name is None:
        out_file_name= f'triaged_{in_file_name}'
    
    in_file= open('../'+in_file_name,"r")
    out_file= open(out_file_name,"w")
    discarded_elements_file= open(f'discarded_{in_file_name}',"w")
    blocker_elements=list()
    discarded_elements=list()
    for line in in_file.readlines():
        discard=False
        try:
            line= json.loads(line)
            value= line.get('value')

            if line.get('message') in ['AWS Access Key ID', 'AWS Secret Access Key', 'AWS Session Token']:
                if 'EXAMPLE' in value: discard= True
            if line.get('message') in ['AWS Access Key ID']:
                if value in ['AKIAJKAUQVHU6X4CODDQ']: discard= True 
            if line.get('message') in ['AWS Secret Access Key']:
                if value in ['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', 'CustomerManagedDatastoreS3StorageSummary', \
                'Scte35SpliceInsertScheduleActionSettings', 'AwsS3BucketServerSideEncryptionByDefault', \
                'ExportEC2InstanceRecommendationsResponse', 'c1dCell2matInconsistentSizesOfLocalParts', \
                'c2dbcBuildFromReplicatedUnsupportedClass', 'transformPointsPackedMatrixInvalidSize3d', \
                'LWMSecondDegreePolynomialRequires6Points', 'HPCServer2008SOFailedToGenerateSOAInputs', \
                'CompressionWithJPEG2000CodecLosslessMode', 'mapBlkInputQuadrilateralVerticesR1c1r4c4', \
                'InvalidColumnsEnteredInRow0numberinteger', 'ImplicitSelectorDimBasedNumIterMismatch1', \
                'CordicATan2UnSignedInputWLGreaterThan125', 'GPUAccelerated2DCanvasImageBufferCreated', \
                'replaceApiregistrationV1APIServiceStatus', 'watchAppsV1DaemonSetListForAllNamespaces', \
                'watchAppsV1beta2NamespacedReplicaSetList', 'createAuthorizationV1SubjectAccessReview', \
                'listBatchV2alpha1CronJobForAllNamespaces', 'replaceRbacAuthorizationV1NamespacedRole', \
                'ExtensionsV1beta1RollingUpdateDeployment', 'R53RResolverEndpointIpAddressAssociation', \
                'EC2SecurityGroupToClientVpnTargetNetwork', 'EC2SecurityGroupToClientVpnTargetNetwork', \
                'seeAdminOrderProductOptionValueDropdown1', 'connectCoreV1GetNamespacedPodPortforward', \
                'watchAppsV1beta1NamespacedDeploymentList', 'deleteExtensionsV1beta1PodSecurityPolicy', \
                'patchRbacAuthorizationV1beta1ClusterRole', 'watchSettingsV1alpha1NamespacedPodPreset', \
                'watchCoreV1EndpointsListForAllNamespaces', 'readAppsV1beta1NamespacedDeploymentScale', \
                'getRbacAuthorizationV1alpha1APIResources', 'watchSchedulingV1alpha1PriorityClassList', \
                'deleteExtensionsV1beta1NamespacedIngress', 'watchRbacAuthorizationV1beta1ClusterRole', \
                'createAppsV1NamespacedControllerRevision', 'readBatchV2alpha1NamespacedCronJobStatus', \
                'readAppsV1beta2NamespacedDeploymentScale', 'aaw1AZ7+OlEEy6FrXkGy0oP2p4BvE/Eeg0L9ucmj']: discard= True
                elif value.upper().startswith('/USR/'): discard= True
                elif value.upper().startswith('INCLUDE/'): discard= True
                elif value.upper().startswith('V1BETA1A/SUBSCRIPTIONS/'): discard= True
                elif value.upper().startswith('GOOGLE'): discard= True
                elif value.upper().startswith('BUILD'): discard= True
                elif value.upper().startswith('RECURSIVE'): discard= True
                elif value.upper().startswith('DATADEP'): discard= True
                elif value.upper().startswith('ASSERT'): discard= True
                elif value.upper().startswith('MATCODE'): discard= True
                elif value.upper().startswith('WAITFOR'): discard= True
                elif value.upper().startswith('J2EE'): discard= True
                elif value.upper().startswith('BEASAML'): discard= True
            if line.get('message') in ['Azure Data']:
                if ('HTTPS://GOLANGROCKSONAZURE') in line.get('key').upper(): discard= True
                elif len(value) <= 10: discard= True
                 # At least a number and a letter
                elif not bool(re.match('^(?=.*[a-zA-Z])(?=.*[0-9])', value)): discard= True
                elif value.upper().endswith('PREVIEW') : discard= True
                elif value in ['AzDataFactoryV2IntegrationRuntimeUpgrade']: discard= True
                elif value.upper().startswith('X86_64'): discard= True
                
            if discard:
                discarded_elements.append(line)
                continue
            else:
                blocker_elements.append(line)
                
            store_triaged_file(line.get('file'))
        except Exception as e:
            print(f"Error triaging blocker: {e}. Line: {line}\n")
    
    blocker_elements= remove_duplicated_key_values(blocker_elements)
    for i in blocker_elements:
        out_file.write(json.dumps(i)+'\n')
    for i in discarded_elements:
        discarded_elements_file.write(json.dumps(i)+'\n')

    in_file.close()
    out_file.close()
    discarded_elements_file.close()

def remove_duplicated_key_values(elements):
    deduplicated_list= elements.copy()
    for elem in elements:
        skipped_once=False
        elem_split_path = split_path_by_dir(elem.get('file'))
        for elem2 in deduplicated_list:
            elem2_split_path = split_path_by_dir(elem2.get('file'))
            # If it's the same image, key, and value remove it
            if elem_split_path[2]==elem2_split_path[2] and elem['key']==elem2['key'] and elem['value']==elem2['value']: 
                if skipped_once:
                    deduplicated_list.remove(elem2)
                else:
                    skipped_once=True
    return deduplicated_list

if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Dockerhub Explorer')
    # requiredGroup = parser.add_argument_group('Required arguments')
    # requiredGroup.add_argument('-f','--file',
    #                             help='File to triage',
    #                             required = True)     
    # parser.add_argument('-o','--output',
    #                     help= 'Output file name',
    #                     default=None)    
    # options= parser.parse_args()                        
    
    if not os.path.exists(triaged_path):
        os.makedirs(triaged_path)
    os.chdir(triaged_path)

    triage_critical_file('critical.txt', None)
    triage_blocker_file('blocker.txt', None)
