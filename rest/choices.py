import pytz

TEMPLATE = (
    ('sysad41', 'SYSAD41'),
    ('adc41', 'ADC41'),
    ('cgn41', 'CGN41'),
    ('tps', 'TPS'),
    ('ssli', 'SSLi'),
) 

CLOUD_REGION = (
    #('westus', 'US West'),
    ('westus2', 'US West 2'),
    #('centralus', 'US Central'),
    #('eastus', 'US East'),
    #('eastus2', 'US East 2'),
    #('eastasia', 'Asia East'),
    ('southeastasia', 'Asia Southeast'),
    #('northcentralus', 'US North Central'),
    #('southcentralus', 'US South Central'),
    ('westeurope', 'Europe West'),
    #('japanwest', 'Japan West'),
    #('japaneast', 'Japan East'),
    #('brazilsouth', 'Brazil South'),
    #('southindia', 'India South'),
    #('brazilsouth', 'Brazil South'),
)

RATECARD_REGION = (
    ('westus', 'US West'),
    ('westus2', 'US West 2'),
    ('centralus', 'US Central'),
    #('eastus', 'US East'),
    #('eastus2', 'US East 2'),
    #('eastasia', 'AP East'),
    ('southeastasia', 'AP Southeast'),
    #('northcentralus', 'US North Central'),
    #('southcentralus', 'US South Central'),
    ('westeurope', 'EU West'),
    #('japanwest', 'JA West'),
    #('japaneast', 'JA East'),
    #('brazilsouth', 'BR South'),
    #('southindia', 'IN South'),
    #('brazilsouth', 'BR South'),
)

STATUS =  (
    ('undeployed', 'Undeployed'),    
    ('deploying', 'Deploying'),    
    ('started', 'Started'),    
    ('starting', 'Starting'),    
    ('stopped', 'Stopped'),    
    ('stopping', 'Stopping'),    
    ('restarting', 'Restarting'),    
    ('delete', 'DELETE'),    
    ('error', 'ERROR'),    
)

TASK_ACTION = (
    ('next_stop', 'Next Stop'),
    ('stop_reminder', 'Stop Reminder Notification'),
    ('auto_start', 'Auto Start'),
    ('auto_stop', 'Auto Stop'),
)

ADD_TASK_ACTION = (
    ('auto_start', 'Auto Start'),
    ('auto_stop', 'Auto Stop'),
)

NEXTSTOP = ()
for i in list(range(1,11)):
    i = str(i)
    new_choice = (i, i)
    NEXTSTOP = NEXTSTOP + (new_choice,)
    
VM_SIZE = ((None, "Please select a template first"),)
    

TIME_ZONE = ()
for zone in pytz.common_timezones:
    new_choice = (zone, zone)
    TIME_ZONE = TIME_ZONE + (new_choice,)
    
        