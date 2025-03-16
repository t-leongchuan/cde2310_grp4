from cde2310_interfaces.srv import ActivateNode
from cde2310_interfaces.srv import NodeFinish

import rclpy
from rclpy.node import Node

class Exploration(Node):
    
    def __init__(self):
        
        # ############# Exploration Node Initialization ############# #
        super().__init__('exploration')
        
        # ############# Server: Handle Activate Exploration Request ############# #
        self.ExplorationServer = self.create_service(ActivateNode, 'activate_exploration', self.activate_exploration_callback)
        
        # ############# Client: Notify Supervisor When Exploration Completes ############# #
        self.ExplorationStatusClient = self.create_client(NodeFinish, 'exploration_finish')
        while not self.ExplorationStatusClient.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.IsExplorationComplete = NodeFinish.Request()
    
    # ############# Client Call: Notify Supervisor About Exploration Completion ############# #
    def is_exploration_complete(self, activate):
        """ Sends a message to Supervisor if exploration is complete or still in progress. """
        self.IsExplorationComplete.activate = activate
        return self.ExplorationStatusClient.call_async(self.IsExplorationComplete)  # FIXED: Corrected attribute reference
    
    # ############# Server Response: Handle Start/Stop Requests from Supervisor ############# #
    def activate_exploration_callback(self, request, response):
        activate = request.activate
        
        if not activate:
            self.get_logger().info('Supervisor has requested to **deactivate exploration**.')
            self.get_logger().info('Simulating Exploration Deactivation...')
            response.message = "Exploration Node Acknowledges: Exploration is deactivated."
            return response
            
        if activate:
            self.get_logger().info('Supervisor has requested to **activate exploration**.')
            self.get_logger().info('Simulating Exploration...')
            response.message = "Exploration Node Acknowledges: Exploration is activated."
            return response

def main():
    rclpy.init()
    exploration = Exploration()

    rclpy.spin(exploration)

    exploration.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
