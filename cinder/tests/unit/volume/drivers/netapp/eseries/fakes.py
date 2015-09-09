# Copyright (c) - 2015, Alex Meade
# Copyright (c) - 2015, Yogesh Kshirsagar
# Copyright (c) - 2015, Michael Price
#  All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import copy
import json

import mock

from cinder.volume import configuration as conf
from cinder.volume.drivers.netapp.eseries import utils
import cinder.volume.drivers.netapp.options as na_opts


def mock_netapp_lib(modules):
    """Inject fake netapp_lib module classes."""
    netapp_lib = mock.Mock()
    netapp_lib.api.rest.rest.WebserviceClient = mock.Mock()
    for module in modules:
        setattr(module, 'netapp_restclient', netapp_lib.api.rest.rest)

MULTIATTACH_HOST_GROUP = {
    'clusterRef': '8500000060080E500023C7340036035F515B78FC',
    'label': utils.MULTI_ATTACH_HOST_GROUP_NAME,
}

FOREIGN_HOST_GROUP = {
    'clusterRef': '8500000060080E500023C7340036035F515B78FD',
    'label': 'FOREIGN HOST GROUP',
}

SSC_POOLS = [
    {
        "poolId": "0400000060080E5000290D8000009C9955828DD2",
        "name": "DDP",
        "pool": {
            "sequenceNum": 2,
            "offline": False,
            "raidLevel": "raidDiskPool",
            "worldWideName": "60080E5000290D8000009C9955828DD2",
            "volumeGroupRef": "0400000060080E5000290D8000009C9955828DD2",
            "reserved1": "000000000000000000000000",
            "reserved2": "",
            "trayLossProtection": False,
            "label": "DDP",
            "state": "complete",
            "spindleSpeedMatch": True,
            "spindleSpeed": 7200,
            "isInaccessible": False,
            "securityType": "none",
            "drawerLossProtection": True,
            "protectionInformationCapable": False,
            "protectionInformationCapabilities": {
                "protectionInformationCapable": True,
                "protectionType": "type2Protection"
            },
            "volumeGroupData": {
                "type": "diskPool",
                "diskPoolData": {
                    "reconstructionReservedDriveCount": 1,
                    "reconstructionReservedAmt": "2992518463488",
                    "reconstructionReservedDriveCountCurrent": 1,
                    "poolUtilizationWarningThreshold": 100,
                    "poolUtilizationCriticalThreshold": 100,
                    "poolUtilizationState": "utilizationOptimal",
                    "unusableCapacity": "0",
                    "degradedReconstructPriority": "high",
                    "criticalReconstructPriority": "highest",
                    "backgroundOperationPriority": "low",
                    "allocGranularity": "4294967296"
                }
            },
            "usage": "standard",
            "driveBlockFormat": "allNative",
            "reservedSpaceAllocated": True,
            "usedSpace": "13653701033984",
            "totalRaidedSpace": "23459111370752",
            "extents": [
                {
                    "sectorOffset": "0",
                    "rawCapacity": "9805410336768",
                    "raidLevel": "raidDiskPool",
                    "volumeGroupRef":
                        "0400000060080E5000290D8000009C9955828DD2",
                    "freeExtentRef":
                        "0301000060080E5000290D8000009C9955828DD2",
                    "reserved1": "000000000000000000000000",
                    "reserved2": ""
                }
            ],
            "largestFreeExtentSize": "9805410336768",
            "raidStatus": "optimal",
            "freeSpace": "9805410336768",
            "drivePhysicalType": "sas",
            "driveMediaType": "hdd",
            "normalizedSpindleSpeed": "spindleSpeed7200",
            "id": "0400000060080E5000290D8000009C9955828DD2",
            "diskPool": True,
            "name": "DDP"
        },
        "flashCacheCapable": True,
        "dataAssuranceCapable": True,
        "encrypted": False,
        "thinProvisioningCapable": True,
        "spindleSpeed": "spindleSpeed7200",
        "raidLevel": "raidDiskPool",
        "availableFreeExtentCapacities": [
            "9805410336768"
        ]
    },
    {
        "poolId": "0400000060080E5000290D8000009CBA55828E96",
        "name": "pool_raid1",
        "pool": {
            "sequenceNum": 6,
            "offline": False,
            "raidLevel": "raid1",
            "worldWideName": "60080E5000290D8000009CBA55828E96",
            "volumeGroupRef": "0400000060080E5000290D8000009CBA55828E96",
            "reserved1": "000000000000000000000000",
            "reserved2": "",
            "trayLossProtection": False,
            "label": "pool_raid1",
            "state": "complete",
            "spindleSpeedMatch": True,
            "spindleSpeed": 10000,
            "isInaccessible": False,
            "securityType": "none",
            "drawerLossProtection": True,
            "protectionInformationCapable": False,
            "protectionInformationCapabilities": {
                "protectionInformationCapable": True,
                "protectionType": "type2Protection"
            },
            "volumeGroupData": {
                "type": "unknown",
                "diskPoolData": None
            },
            "usage": "standard",
            "driveBlockFormat": "allNative",
            "reservedSpaceAllocated": True,
            "usedSpace": "2978559819776",
            "totalRaidedSpace": "6662444097536",
            "extents": [
                {
                    "sectorOffset": "387891200",
                    "rawCapacity": "3683884277760",
                    "raidLevel": "raid1",
                    "volumeGroupRef":
                        "0400000060080E5000290D8000009CBA55828E96",
                    "freeExtentRef":
                        "030000B360080E5000290D8000009CBA55828E96",
                    "reserved1": "000000000000000000000000",
                    "reserved2": ""
                }
            ],
            "largestFreeExtentSize": "3683884277760",
            "raidStatus": "optimal",
            "freeSpace": "3683884277760",
            "drivePhysicalType": "sas",
            "driveMediaType": "hdd",
            "normalizedSpindleSpeed": "spindleSpeed10k",
            "id": "0400000060080E5000290D8000009CBA55828E96",
            "diskPool": False,
            "name": "pool_raid1"
        },
        "flashCacheCapable": False,
        "dataAssuranceCapable": True,
        "encrypted": False,
        "thinProvisioningCapable": False,
        "spindleSpeed": "spindleSpeed10k",
        "raidLevel": "raid1",
        "availableFreeExtentCapacities": [
            "3683884277760"
        ]
    },
    {
        "poolId": "0400000060080E5000290D8000009CAB55828E51",
        "name": "pool_raid6",
        "pool": {
            "sequenceNum": 3,
            "offline": False,
            "raidLevel": "raid6",
            "worldWideName": "60080E5000290D8000009CAB55828E51",
            "volumeGroupRef": "0400000060080E5000290D8000009CAB55828E51",
            "reserved1": "000000000000000000000000",
            "reserved2": "",
            "trayLossProtection": False,
            "label": "pool_raid6",
            "state": "complete",
            "spindleSpeedMatch": True,
            "spindleSpeed": 15000,
            "isInaccessible": False,
            "securityType": "enabled",
            "drawerLossProtection": False,
            "protectionInformationCapable": False,
            "protectionInformationCapabilities": {
                "protectionInformationCapable": True,
                "protectionType": "type2Protection"
            },
            "volumeGroupData": {
                "type": "unknown",
                "diskPoolData": None
            },
            "usage": "standard",
            "driveBlockFormat": "allNative",
            "reservedSpaceAllocated": True,
            "usedSpace": "16413217521664",
            "totalRaidedSpace": "16637410312192",
            "extents": [
                {
                    "sectorOffset": "1144950784",
                    "rawCapacity": "224192790528",
                    "raidLevel": "raid6",
                    "volumeGroupRef":
                        "0400000060080E5000290D8000009CAB55828E51",
                    "freeExtentRef":
                        "0300005960080E5000290D8000009CAB55828E51",
                    "reserved1": "000000000000000000000000",
                    "reserved2": ""
                }
            ],
            "largestFreeExtentSize": "224192790528",
            "raidStatus": "optimal",
            "freeSpace": "224192790528",
            "drivePhysicalType": "sas",
            "driveMediaType": "hdd",
            "normalizedSpindleSpeed": "spindleSpeed15k",
            "id": "0400000060080E5000290D8000009CAB55828E51",
            "diskPool": False,
            "name": "pool_raid6"
        },
        "flashCacheCapable": False,
        "dataAssuranceCapable": True,
        "encrypted": True,
        "thinProvisioningCapable": False,
        "spindleSpeed": "spindleSpeed15k",
        "raidLevel": "raid6",
        "availableFreeExtentCapacities": [
            "224192790528"
        ]
    }
]

STORAGE_POOLS = [ssc_pool['pool'] for ssc_pool in SSC_POOLS]

VOLUMES = [
    {
        "offline": False,
        "extremeProtection": False,
        "volumeHandle": 2,
        "raidLevel": "raid0",
        "sectorOffset": "0",
        "worldWideName": "60080E50002998A00000945355C37C19",
        "label": "1",
        "blkSize": 512,
        "capacity": "10737418240",
        "reconPriority": 1,
        "segmentSize": 131072,
        "action": "initializing",
        "cache": {
            "cwob": False,
            "enterpriseCacheDump": False,
            "mirrorActive": True,
            "mirrorEnable": True,
            "readCacheActive": True,
            "readCacheEnable": True,
            "writeCacheActive": True,
            "writeCacheEnable": True,
            "cacheFlushModifier": "flush10Sec",
            "readAheadMultiplier": 1
        },
        "mediaScan": {
            "enable": False,
            "parityValidationEnable": False
        },
        "volumeRef": "0200000060080E50002998A00000945355C37C19",
        "status": "optimal",
        "volumeGroupRef": "0400000060080E50002998A00000945255C37C14",
        "currentManager": "070000000000000000000001",
        "preferredManager": "070000000000000000000001",
        "perms": {
            "mapToLUN": True,
            "snapShot": True,
            "format": True,
            "reconfigure": True,
            "mirrorPrimary": True,
            "mirrorSecondary": True,
            "copySource": True,
            "copyTarget": True,
            "readable": True,
            "writable": True,
            "rollback": True,
            "mirrorSync": True,
            "newImage": True,
            "allowDVE": True,
            "allowDSS": True,
            "concatVolumeMember": True,
            "flashReadCache": True,
            "asyncMirrorPrimary": True,
            "asyncMirrorSecondary": True,
            "pitGroup": True,
            "cacheParametersChangeable": True,
            "allowThinManualExpansion": False,
            "allowThinGrowthParametersChange": False,
            "allowVaulting": False,
            "allowRestore": False
        },
        "mgmtClientAttribute": 0,
        "dssPreallocEnabled": True,
        "dssMaxSegmentSize": 2097152,
        "preReadRedundancyCheckEnabled": False,
        "protectionInformationCapable": False,
        "protectionType": "type1Protection",
        "applicationTagOwned": False,
        "untrustworthy": 0,
        "volumeUse": "standardVolume",
        "volumeFull": False,
        "volumeCopyTarget": False,
        "volumeCopySource": False,
        "pitBaseVolume": False,
        "asyncMirrorTarget": False,
        "asyncMirrorSource": False,
        "remoteMirrorSource": False,
        "remoteMirrorTarget": False,
        "diskPool": False,
        "flashCached": False,
        "increasingBy": "0",
        "metadata": [],
        "dataAssurance": True,
        "name": "1",
        "id": "0200000060080E50002998A00000945355C37C19",
        "wwn": "60080E50002998A00000945355C37C19",
        "objectType": "volume",
        "mapped": False,
        "preferredControllerId": "070000000000000000000001",
        "totalSizeInBytes": "10737418240",
        "onlineVolumeCopy": False,
        "listOfMappings": [],
        "currentControllerId": "070000000000000000000001",
        "cacheSettings": {
            "cwob": False,
            "enterpriseCacheDump": False,
            "mirrorActive": True,
            "mirrorEnable": True,
            "readCacheActive": True,
            "readCacheEnable": True,
            "writeCacheActive": True,
            "writeCacheEnable": True,
            "cacheFlushModifier": "flush10Sec",
            "readAheadMultiplier": 1
        },
        "thinProvisioned": False
    },
    {
        "volumeHandle": 16385,
        "worldWideName": "60080E500029347000001D7B55C3791E",
        "label": "2",
        "allocationGranularity": 128,
        "capacity": "53687091200",
        "reconPriority": 1,
        "volumeRef": "3A00000060080E500029347000001D7B55C3791E",
        "status": "optimal",
        "repositoryRef": "3600000060080E500029347000001D7955C3791D",
        "currentManager": "070000000000000000000002",
        "preferredManager": "070000000000000000000002",
        "perms": {
            "mapToLUN": True,
            "snapShot": False,
            "format": True,
            "reconfigure": False,
            "mirrorPrimary": False,
            "mirrorSecondary": False,
            "copySource": True,
            "copyTarget": False,
            "readable": True,
            "writable": True,
            "rollback": True,
            "mirrorSync": True,
            "newImage": True,
            "allowDVE": True,
            "allowDSS": True,
            "concatVolumeMember": False,
            "flashReadCache": True,
            "asyncMirrorPrimary": True,
            "asyncMirrorSecondary": True,
            "pitGroup": True,
            "cacheParametersChangeable": True,
            "allowThinManualExpansion": False,
            "allowThinGrowthParametersChange": False,
            "allowVaulting": False,
            "allowRestore": False
        },
        "mgmtClientAttribute": 0,
        "preReadRedundancyCheckEnabled": False,
        "protectionType": "type0Protection",
        "applicationTagOwned": True,
        "maxVirtualCapacity": "69269232549888",
        "initialProvisionedCapacity": "4294967296",
        "currentProvisionedCapacity": "4294967296",
        "provisionedCapacityQuota": "55834574848",
        "growthAlertThreshold": 85,
        "expansionPolicy": "automatic",
        "volumeCache": {
            "cwob": False,
            "enterpriseCacheDump": False,
            "mirrorActive": True,
            "mirrorEnable": True,
            "readCacheActive": True,
            "readCacheEnable": True,
            "writeCacheActive": True,
            "writeCacheEnable": True,
            "cacheFlushModifier": "flush10Sec",
            "readAheadMultiplier": 0
        },
        "offline": False,
        "volumeFull": False,
        "volumeGroupRef": "0400000060080E50002998A00000945155C37C08",
        "blkSize": 512,
        "storageVolumeRef": "0200000060080E500029347000001D7855C3791D",
        "volumeCopyTarget": False,
        "volumeCopySource": False,
        "pitBaseVolume": False,
        "asyncMirrorTarget": False,
        "asyncMirrorSource": False,
        "remoteMirrorSource": False,
        "remoteMirrorTarget": False,
        "flashCached": False,
        "mediaScan": {
            "enable": False,
            "parityValidationEnable": False
        },
        "metadata": [],
        "dataAssurance": False,
        "name": "2",
        "id": "3A00000060080E500029347000001D7B55C3791E",
        "wwn": "60080E500029347000001D7B55C3791E",
        "objectType": "thinVolume",
        "mapped": False,
        "diskPool": True,
        "preferredControllerId": "070000000000000000000002",
        "totalSizeInBytes": "53687091200",
        "onlineVolumeCopy": False,
        "listOfMappings": [],
        "currentControllerId": "070000000000000000000002",
        "segmentSize": 131072,
        "cacheSettings": {
            "cwob": False,
            "enterpriseCacheDump": False,
            "mirrorActive": True,
            "mirrorEnable": True,
            "readCacheActive": True,
            "readCacheEnable": True,
            "writeCacheActive": True,
            "writeCacheEnable": True,
            "cacheFlushModifier": "flush10Sec",
            "readAheadMultiplier": 0
        },
        "thinProvisioned": True
    }
]

VOLUME = VOLUMES[0]

STORAGE_POOL = {
    'label': 'DDP',
    'volumeGroupRef': 'fakevolgroupref',
    'raidLevel': 'raidDiskPool',
    'usedSpace': '16413217521664',
    'totalRaidedSpace': '16637410312192',
}

INITIATOR_NAME = 'iqn.1998-01.com.vmware:localhost-28a58148'
INITIATOR_NAME_2 = 'iqn.1998-01.com.vmware:localhost-28a58149'
INITIATOR_NAME_3 = 'iqn.1998-01.com.vmware:localhost-28a58150'
WWPN = '20130080E5322230'
WWPN_2 = '20230080E5322230'

FC_TARGET_WWPNS = [
    '500a098280feeba5',
    '500a098290feeba5',
    '500a098190feeba5',
    '500a098180feeba5'
]

FC_I_T_MAP = {
    '20230080E5322230': [
        '500a098280feeba5',
        '500a098290feeba5'
    ],
    '20130080E5322230': [
        '500a098190feeba5',
        '500a098180feeba5'
    ]
}

FC_FABRIC_MAP = {
    'fabricB': {
        'target_port_wwn_list': [
            '500a098190feeba5',
            '500a098180feeba5'
        ],
        'initiator_port_wwn_list': [
            '20130080E5322230'
        ]
    },
    'fabricA': {
        'target_port_wwn_list': [
            '500a098290feeba5',
            '500a098280feeba5'
        ],
        'initiator_port_wwn_list': [
            '20230080E5322230'
        ]
    }
}

HOST = {
    'isSAControlled': False,
    'confirmLUNMappingCreation': False,
    'label': 'stlrx300s7-55',
    'isLargeBlockFormatHost': False,
    'clusterRef': '8500000060080E500023C7340036035F515B78FC',
    'protectionInformationCapableAccessMethod': False,
    'ports': [],
    'hostRef': '8400000060080E500023C73400300381515BFBA3',
    'hostTypeIndex': 6,
    'hostSidePorts': [{
        'label': 'NewStore',
        'type': 'iscsi',
        'address': INITIATOR_NAME}]
}
HOST_2 = {
    'isSAControlled': False,
    'confirmLUNMappingCreation': False,
    'label': 'stlrx300s7-55',
    'isLargeBlockFormatHost': False,
    'clusterRef': utils.NULL_REF,
    'protectionInformationCapableAccessMethod': False,
    'ports': [],
    'hostRef': '8400000060080E500023C73400300381515BFBA5',
    'hostTypeIndex': 6,
    'hostSidePorts': [{
        'label': 'NewStore', 'type': 'iscsi',
        'address': INITIATOR_NAME_2}]
}
# HOST_3 has all lun_ids in use.
HOST_3 = {
    'isSAControlled': False,
    'confirmLUNMappingCreation': False,
    'label': 'stlrx300s7-55',
    'isLargeBlockFormatHost': False,
    'clusterRef': '8500000060080E500023C73400360351515B78FC',
    'protectionInformationCapableAccessMethod': False,
    'ports': [],
    'hostRef': '8400000060080E501023C73400800381515BFBA5',
    'hostTypeIndex': 6,
    'hostSidePorts': [{
        'label': 'NewStore', 'type': 'iscsi',
        'address': INITIATOR_NAME_3}],
}


VOLUME_MAPPING = {
    'lunMappingRef': '8800000000000000000000000000000000000000',
    'lun': 0,
    'ssid': 16384,
    'perms': 15,
    'volumeRef': VOLUME['volumeRef'],
    'type': 'all',
    'mapRef': HOST['hostRef']
}
# VOLUME_MAPPING_3 corresponding to HOST_3 has all lun_ids in use.
VOLUME_MAPPING_3 = {
    'lunMappingRef': '8800000000000000000000000000000000000000',
    'lun': range(255),
    'ssid': 16384,
    'perms': 15,
    'volumeRef': VOLUME['volumeRef'],
    'type': 'all',
    'mapRef': HOST_3['hostRef'],
}

VOLUME_MAPPING_TO_MULTIATTACH_GROUP = copy.deepcopy(VOLUME_MAPPING)
VOLUME_MAPPING_TO_MULTIATTACH_GROUP.update(
    {'mapRef': MULTIATTACH_HOST_GROUP['clusterRef']}
)

STORAGE_SYSTEM = {
    'freePoolSpace': 11142431623168,
    'driveCount': 24,
    'hostSparesUsed': 0, 'id':
    '1fa6efb5-f07b-4de4-9f0e-52e5f7ff5d1b',
    'hotSpareSizeAsString': '0', 'wwn':
    '60080E500023C73400000000515AF323',
    'parameters': {
        'minVolSize': 1048576, 'maxSnapshotsPerBase': 16,
        'maxDrives': 192,
        'maxVolumes': 512,
        'maxVolumesPerGroup': 256,
        'maxMirrors': 0,
        'maxMappingsPerVolume': 1,
        'maxMappableLuns': 256,
        'maxVolCopys': 511,
        'maxSnapshots': 256
    }, 'hotSpareCount': 0,
    'hostSpareCountInStandby': 0,
    'status': 'needsattn',
    'trayCount': 1,
    'usedPoolSpaceAsString': '5313000380416',
    'ip2': '10.63.165.216',
    'ip1': '10.63.165.215',
    'freePoolSpaceAsString': '11142431623168',
    'types': 'SAS',
    'name': 'stle2600-7_8',
    'hotSpareSize': 0,
    'usedPoolSpace': 5313000380416,
    'driveTypes': ['sas'],
    'unconfiguredSpaceByDriveType': {},
    'unconfiguredSpaceAsStrings': '0',
    'model': '2650',
    'unconfiguredSpace': 0
}

SNAPSHOT_GROUP = {
    'status': 'optimal',
    'autoDeleteLimit': 0,
    'maxRepositoryCapacity': '-65536',
    'rollbackStatus': 'none',
    'unusableRepositoryCapacity': '0',
    'pitGroupRef':
    '3300000060080E500023C7340000098D5294AC9A',
    'clusterSize': 65536,
    'label': 'C6JICISVHNG2TFZX4XB5ZWL7O',
    'maxBaseCapacity': '476187142128128',
    'repositoryVolume': '3600000060080E500023BB3400001FA952CEF12C',
    'fullWarnThreshold': 99,
    'repFullPolicy': 'purgepit',
    'action': 'none',
    'rollbackPriority': 'medium',
    'creationPendingStatus': 'none',
    'consistencyGroupRef': '0000000000000000000000000000000000000000',
    'volumeHandle': 49153,
    'consistencyGroup': False,
    'baseVolume': '0200000060080E500023C734000009825294A534'
}

SNAPSHOT_IMAGE = {
    'status': 'optimal',
    'pitCapacity': '2147483648',
    'pitTimestamp': '1389315375',
    'pitGroupRef': '3300000060080E500023C7340000098D5294AC9A',
    'creationMethod': 'user',
    'repositoryCapacityUtilization': '2818048',
    'activeCOW': True,
    'isRollbackSource': False,
    'pitRef': '3400000060080E500023BB3400631F335294A5A8',
    'pitSequenceNumber': '19'
}

HARDWARE_INVENTORY = {
    'iscsiPorts': [
        {
            'controllerId':
            '070000000000000000000002',
            'ipv4Enabled': True,
            'ipv4Data': {
                'ipv4Address': '0.0.0.0',
                'ipv4AddressConfigMethod':
                'configStatic',
                'ipv4VlanId': {
                    'isEnabled': False,
                    'value': 0
                },
                'ipv4AddressData': {
                    'ipv4Address': '172.20.123.66',
                    'ipv4SubnetMask': '255.255.255.0',
                    'configState': 'configured',
                    'ipv4GatewayAddress': '0.0.0.0'
                }
            },
            'tcpListenPort': 3260,
            'interfaceRef': '2202040000000000000000000000000000000000',
            'iqn': 'iqn.1992-01.com.lsi:2365.60080e500023c73400000000515af323'
        }
    ],
    'fibrePorts': [
        {
            "channel": 1,
            "loopID": 126,
            "speed": 800,
            "hardAddress": 6,
            "nodeName": "20020080E5322230",
            "portName": "20130080E5322230",
            "portId": "011700",
            "topology": "fabric",
            "part": "PM8032          ",
            "revision": 8,
            "chanMiswire": False,
            "esmMiswire": False,
            "linkStatus": "up",
            "isDegraded": False,
            "speedControl": "auto",
            "maxSpeed": 800,
            "speedNegError": False,
            "reserved1": "000000000000000000000000",
            "reserved2": "",
            "ddsChannelState": 0,
            "ddsStateReason": 0,
            "ddsStateWho": 0,
            "isLocal": True,
            "channelPorts": [],
            "currentInterfaceSpeed": "speed8gig",
            "maximumInterfaceSpeed": "speed8gig",
            "interfaceRef": "2202020000000000000000000000000000000000",
            "physicalLocation": {
                "trayRef": "0000000000000000000000000000000000000000",
                "slot": 0,
                "locationParent": {
                    "refType": "generic",
                    "controllerRef": None,
                    "symbolRef": "0000000000000000000000000000000000000000",
                    "typedReference": None
                },
                "locationPosition": 0
            },
            "isTrunkCapable": False,
            "trunkMiswire": False,
            "protectionInformationCapable": True,
            "controllerId": "070000000000000000000002",
            "interfaceId": "2202020000000000000000000000000000000000",
            "addressId": "20130080E5322230",
            "niceAddressId": "20:13:00:80:E5:32:22:30"
        },
        {
            "channel": 2,
            "loopID": 126,
            "speed": 800,
            "hardAddress": 7,
            "nodeName": "20020080E5322230",
            "portName": "20230080E5322230",
            "portId": "011700",
            "topology": "fabric",
            "part": "PM8032          ",
            "revision": 8,
            "chanMiswire": False,
            "esmMiswire": False,
            "linkStatus": "up",
            "isDegraded": False,
            "speedControl": "auto",
            "maxSpeed": 800,
            "speedNegError": False,
            "reserved1": "000000000000000000000000",
            "reserved2": "",
            "ddsChannelState": 0,
            "ddsStateReason": 0,
            "ddsStateWho": 0,
            "isLocal": True,
            "channelPorts": [],
            "currentInterfaceSpeed": "speed8gig",
            "maximumInterfaceSpeed": "speed8gig",
            "interfaceRef": "2202030000000000000000000000000000000000",
            "physicalLocation": {
                "trayRef": "0000000000000000000000000000000000000000",
                "slot": 0,
                "locationParent": {
                    "refType": "generic",
                    "controllerRef": None,
                    "symbolRef": "0000000000000000000000000000000000000000",
                    "typedReference": None
                },
                "locationPosition": 0
            },
            "isTrunkCapable": False,
            "trunkMiswire": False,
            "protectionInformationCapable": True,
            "controllerId": "070000000000000000000002",
            "interfaceId": "2202030000000000000000000000000000000000",
            "addressId": "20230080E5322230",
            "niceAddressId": "20:23:00:80:E5:32:22:30"
        },
    ]
}

FAKE_RESOURCE_URL = '/devmgr/v2/devmgr/utils/about'
FAKE_APP_VERSION = '2015.2|2015.2.dev59|vendor|Linux-3.13.0-24-generic'
FAKE_BACKEND = 'eseriesiSCSI'
FAKE_CINDER_HOST = 'ubuntu-1404'
FAKE_SERIAL_NUMBERS = ['021436000943', '021436001321']
FAKE_SERIAL_NUMBER = ['021436001321']
FAKE_DEFAULT_SERIAL_NUMBER = ['unknown', 'unknown']
FAKE_DEFAULT_MODEL = 'unknown'
FAKE_ABOUT_RESPONSE = {
    'runningAsProxy': True,
    'version': '01.53.9010.0005',
    'systemId': 'a89355ab-692c-4d4a-9383-e249095c3c0',
}

FAKE_CONTROLLERS = [
    {'serialNumber': FAKE_SERIAL_NUMBERS[0], 'modelName': '2752'},
    {'serialNumber': FAKE_SERIAL_NUMBERS[1], 'modelName': '2752'}]

FAKE_SINGLE_CONTROLLER = [{'serialNumber': FAKE_SERIAL_NUMBERS[1]}]

FAKE_KEY = ('openstack-%s-%s-%s' % (FAKE_CINDER_HOST, FAKE_SERIAL_NUMBERS[0],
                                    FAKE_SERIAL_NUMBERS[1]))

FAKE_ASUP_DATA = {
    'category': 'provisioning',
    'app-version': FAKE_APP_VERSION,
    'event-source': 'Cinder driver NetApp_iSCSI_ESeries',
    'event-description': 'OpenStack Cinder connected to E-Series proxy',
    'system-version': '08.10.15.00',
    'computer-name': FAKE_CINDER_HOST,
    'model': FAKE_CONTROLLERS[0]['modelName'],
    'controller2-serial': FAKE_CONTROLLERS[1]['serialNumber'],
    'controller1-serial': FAKE_CONTROLLERS[0]['serialNumber'],
    'operating-mode': 'proxy',
}
FAKE_POST_INVOKE_DATA = ('POST', '/key-values/%s' % FAKE_KEY,
                         json.dumps(FAKE_ASUP_DATA))

VOLUME_COPY_JOB = {
    "status": "complete",
    "cloneCopy": True,
    "pgRef": "3300000060080E500023C73400000ACA52D29454",
    "volcopyHandle": 49160,
    "idleTargetWriteProt": True,
    "copyPriority": "priority2",
    "volcopyRef": "1800000060080E500023C73400000ACF52D29466",
    "worldWideName": "60080E500023C73400000ACF52D29466",
    "copyCompleteTime": "0",
    "sourceVolume": "3500000060080E500023C73400000ACE52D29462",
    "currentManager": "070000000000000000000002",
    "copyStartTime": "1389551671",
    "reserved1": "00000000",
    "targetVolume": "0200000060080E500023C73400000A8C52D10675",
}

FAKE_ENDPOINT_HTTP = 'http://host:80/endpoint'

FAKE_ENDPOINT_HTTPS = 'https://host:8443/endpoint'

FAKE_CLIENT_PARAMS = {
    'scheme': 'http',
    'host': '127.0.0.1',
    'port': 8080,
    'service_path': '/devmgr/vn',
    'username': 'rw',
    'password': 'rw',
}


def create_configuration_eseries():
    config = conf.Configuration(None)
    config.append_config_values(na_opts.netapp_connection_opts)
    config.append_config_values(na_opts.netapp_transport_opts)
    config.append_config_values(na_opts.netapp_basicauth_opts)
    config.append_config_values(na_opts.netapp_provisioning_opts)
    config.append_config_values(na_opts.netapp_eseries_opts)
    config.netapp_storage_protocol = 'iscsi'
    config.netapp_login = 'rw'
    config.netapp_password = 'rw'
    config.netapp_server_hostname = '127.0.0.1'
    config.netapp_transport_type = 'http'
    config.netapp_server_port = '8080'
    config.netapp_storage_pools = 'DDP'
    config.netapp_storage_family = 'eseries'
    config.netapp_sa_password = 'saPass'
    config.netapp_controller_ips = '10.11.12.13,10.11.12.14'
    config.netapp_webservice_path = '/devmgr/v2'
    config.netapp_enable_multiattach = False
    return config


def deepcopy_return_value_method_decorator(fn):
    """Returns a deepcopy of the returned value of the wrapped function."""
    def decorator(*args, **kwargs):
        return copy.deepcopy(fn(*args, **kwargs))

    return decorator


def deepcopy_return_value_class_decorator(cls):
    """Wraps 'non-protected' methods of a class with decorator.

    Wraps all 'non-protected' methods of a class with the
    deepcopy_return_value_method_decorator decorator.
    """
    class NewClass(cls):
        def __getattribute__(self, attr_name):
            obj = super(NewClass, self).__getattribute__(attr_name)
            if (hasattr(obj, '__call__') and not attr_name.startswith('_')
                    and not isinstance(obj, mock.Mock)):
                return deepcopy_return_value_method_decorator(obj)
            return obj

    return NewClass


@deepcopy_return_value_class_decorator
class FakeEseriesClient(object):

    def __init__(self, *args, **kwargs):
        pass

    def list_storage_pools(self):
        return STORAGE_POOLS

    def register_storage_system(self, *args, **kwargs):
        return {
            'freePoolSpace': '17055871480319',
            'driveCount': 24,
            'wwn': '60080E500023C73400000000515AF323',
            'id': '1',
            'hotSpareSizeAsString': '0',
            'hostSparesUsed': 0,
            'types': '',
            'hostSpareCountInStandby': 0,
            'status': 'optimal',
            'trayCount': 1,
            'usedPoolSpaceAsString': '37452115456',
            'ip2': '10.63.165.216',
            'ip1': '10.63.165.215',
            'freePoolSpaceAsString': '17055871480319',
            'hotSpareCount': 0,
            'hotSpareSize': '0',
            'name': 'stle2600-7_8',
            'usedPoolSpace': '37452115456',
            'driveTypes': ['sas'],
            'unconfiguredSpaceByDriveType': {},
            'unconfiguredSpaceAsStrings': '0',
            'model': '2650',
            'unconfiguredSpace': '0'
        }

    def list_volume(self, volume_id):
        return VOLUME

    def list_volumes(self):
        return [VOLUME]

    def delete_volume(self, vol):
        pass

    def create_host_group(self, name):
        return MULTIATTACH_HOST_GROUP

    def get_host_group(self, ref):
        return MULTIATTACH_HOST_GROUP

    def list_host_groups(self):
        return [MULTIATTACH_HOST_GROUP]

    def get_host_group_by_name(self, name, *args, **kwargs):
        host_groups = self.list_host_groups()
        return [host_group for host_group in host_groups
                if host_group['label'] == name][0]

    def set_host_group_for_host(self, *args, **kwargs):
        pass

    def create_host_with_ports(self, *args, **kwargs):
        return HOST

    def list_hosts(self):
        return [HOST, HOST_2]

    def get_host(self, *args, **kwargs):
        return HOST

    def create_volume_mapping(self, *args, **kwargs):
        return VOLUME_MAPPING

    def get_volume_mappings(self):
        return [VOLUME_MAPPING]

    def get_volume_mappings_for_volume(self, volume):
        return [VOLUME_MAPPING]

    def get_volume_mappings_for_host(self, host_ref):
        return [VOLUME_MAPPING]

    def get_volume_mappings_for_host_group(self, hg_ref):
        return [VOLUME_MAPPING]

    def delete_volume_mapping(self):
        return

    def move_volume_mapping_via_symbol(self, map_ref, to_ref, lun_id):
        return {'lun': lun_id}

    def list_storage_system(self):
        return STORAGE_SYSTEM

    def list_storage_systems(self):
        return [STORAGE_SYSTEM]

    def list_snapshot_groups(self):
        return [SNAPSHOT_GROUP]

    def list_snapshot_images(self):
        return [SNAPSHOT_IMAGE]

    def list_host_types(self):
        return [
            {
                'id': '4',
                'code': 'AIX',
                'name': 'AIX',
                'index': 4
            },
            {
                'id': '5',
                'code': 'IRX',
                'name': 'IRX',
                'index': 5
            },
            {
                'id': '6',
                'code': 'LnxALUA',
                'name': 'LnxALUA',
                'index': 6
            }
        ]

    def list_hardware_inventory(self):
        return HARDWARE_INVENTORY

    def get_eseries_api_info(self, verify=False):
        return 'Proxy', '1.53.9010.0005'

    def set_counter(self, key):
        pass

    def add_autosupport_data(self, *args):
        pass

    def get_serial_numbers(self):
        pass

    def get_model_name(self):
        pass

    def api_operating_mode(self):
        pass

    def get_firmware_version(self):
        return FAKE_POST_INVOKE_DATA["system-version"]

    def create_volume_copy_job(self, *args, **kwargs):
        return VOLUME_COPY_JOB

    def list_vol_copy_job(self, *args, **kwargs):
        return VOLUME_COPY_JOB

    def delete_vol_copy_job(self, *args, **kwargs):
        pass

    def delete_snapshot_volume(self, *args, **kwargs):
        pass

    def list_target_wwpns(self, *args, **kwargs):
        return [WWPN_2]
