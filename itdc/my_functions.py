from diagrams import Diagram,Cluster
from diagrams.onprem.compute import Server
from diagrams.azure.compute import VM,VMWindows
from diagrams.onprem.network import Internet
from diagrams.generic.storage import Storage
from diagrams.generic.network import Firewall,Switch
from diagrams.custom import Custom
import os
from itdb.settings import BASE_DIR
from .models import Asset

# Function to draw server structure diagram
def draw_diagram(location):
    #Create address to store diagram
    filename = os.path.join(BASE_DIR,'static','imgs',location + '_server_diagram')

    with Diagram(location, direction="BT", filename=filename,show=False): 

        # Create internet node
        internet = Internet('Internet')

        # Create fireall node
        firewall = Firewall('firewall')

        # Connect internet with firewall
        internet - firewall

        # Create switch node
        switch = Switch('switch')

        # Connect firewall with switch
        firewall - switch
        
        #Create server nodes
        with Cluster('Servers'):
            # Get cluster list
            cluster_list = Asset.objects.filter(category='cluster',location=location,is_active=True)
            if cluster_list:
                #Create cluster             
                for cluster in cluster_list:
                    # Get cluster hosts
                    cluster_host_list = Asset.objects.filter(category='pm',container=cluster,is_active=True)
                    # Get storage for cluster
                    cluster_storage_list = Asset.objects.filter(category='storage',container=cluster,is_active=True)
                    # Get vms for cluster
                    cluster_vm_list = Asset.objects.filter(category='vm',container=cluster,is_active=True)
                    #Define list to store cluster host nodes
                    cluster_host_nodes = []
                    with Cluster(cluster.name):
                        if cluster_storage_list:
                            # Create storage nodes
                            for storage in cluster_storage_list:
                                cluster_host_nodes.append(Custom(storage.name,os.path.join(BASE_DIR,'diagram_icon','storage.png')))
                        if cluster_host_list:
                            # Create host nodes
                            for host in cluster_host_list:
                                cluster_host_nodes.append(Custom(host.name,os.path.join(BASE_DIR,'diagram_icon','server.png')))
                    # Connect switch with cluster hosts
                    switch - cluster_host_nodes
    
                # Create vm for cluster
                if cluster_vm_list:
                    with Cluster('VM in ' + cluster.name):                   
                        for vm in cluster_vm_list:
                            # Create vm and connect to hosts
                            if not vm.is_poweron:
                                cluster_host_nodes - VM(vm.name)
                            else:
                                cluster_host_nodes - VMWindows(vm.name)
                
            # Create physical machine nodes
            #Get host list
            pm_list = Asset.objects.filter(category='pm',location=location,container=None,is_active=True)
            if pm_list :
                for pm in pm_list:
                    # Get vms for host
                    vm_list = Asset.objects.filter(category='vm',container=pm,is_active=True)
                    pm_node = Custom(pm.name,os.path.join(BASE_DIR,'diagram_icon','server.png'))
                    # Connect switch with host
                    switch - pm_node

                    #Create vm for pm host
                    if vm_list:      
                        with Cluster('VM in ' + pm.name):
                            for vm in vm_list:
                                # Create vm and connect to host
                                if not vm.is_poweron:
                                    pm_node - VM(vm.name)
                                else:
                                    pm_node - VMWindows(vm.name)





