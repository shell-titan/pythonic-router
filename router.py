import scapy.all as scapy
import threading
import time
import matplotlib.pyplot as plt
from collections import deque

# Global variable for packet data (for visualization)
packet_data = deque(maxlen=100)  # Adjust maxlen as needed

def packet_forwarder(packet, destination_interface):
    """
    Forward packets from one interface to another.
    :param packet: The packet to forward
    :param destination_interface: The interface through which the packet should be forwarded
    """
    try:
        # Send the packet out of the destination interface
        scapy.sendp(packet, iface=destination_interface, verbose=False)
        
        # Append packet length to the deque for visualization
        packet_length = len(packet)
        packet_data.append(packet_length)
        print(f"Packet forwarded. Length: {packet_length}")
        
    except Exception as e:
        print(f"Error forwarding packet: {e}")

def packet_monitor(source_interface, destination_interface):
    """
    Monitor packets on the specified interface and forward them.
    :param source_interface: The interface to monitor for packets
    :param destination_interface: The interface to forward packets to
    """
    scapy.sniff(iface=source_interface, prn=lambda packet: packet_forwarder(packet, destination_interface))

def visualize_packets():
    """
    Visualize packet activity in real-time.
    """
    global packet_data
    
    print(f"Packet data: {packet_data}")
    print(f"Number of packets: {len(packet_data)}")
    
    fig, ax = plt.subplots()
    ax.plot(packet_data)
    ax.set_ylabel('Packet Data')
    ax.set_xlabel('Time (seconds)')
    ax.set_title('Packet Activity')

    plt.show()

def main():
    source_interface = "wlan0"  # Change to the correct interface name
    destination_interface = "veth1"  # Change to the correct interface name
    
    # Start packet monitoring and forwarding in separate threads
    monitor_thread = threading.Thread(target=packet_monitor, args=(source_interface, destination_interface))
    monitor_thread.start()
    
    visualize_packets()  # Start packet visualization
    
    # Wait for the monitoring thread to finish (if ever)
    monitor_thread.join()

if __name__ == "__main__":
    main()
