# Cart Pendulum System Simulator

This project was created to simulate a cart-pendulum system given specified parameters including properties of the cart and pendulum as well as the initial state of the system. The simulation is run with a GUI, allowing the user to change system or simulation parameters, pause the simulation at anytime, introduce forcing, and more. 

![GUI and simulation screenshot](https://github.com/BrandonBNguyen/Cart-Pendulum-Simulator/blob/main/screenshots/showcase.gif)

## Theory

The cart-pendulum system is governed by the following equations of motion.

![Eq1](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cleft%28%20m_c%20&plus;%20m_p%20%5Cright%29%20%5Cddot%7Bx%7D%20-%20m_p%20l%20%5Cddot%7B%5Ctheta%7D%20%5Ccos%5Ctheta%20&plus;%20m_p%20l%20%5Cdot%7B%5Ctheta%7D%5E2%20%5Csin%5Ctheta%20%3D%20u)
![Eq2](https://latex.codecogs.com/gif.latex?%5CLARGE%20-m_p%20l%20%5Cddot%7Bx%7D%20%5Ccos%5Ctheta%20&plus;%20%5Cleft%28I_p%20&plus;%20m_p%20l%20%5E2%20%5Cright%29%5Cddot%7B%5Ctheta%7D-m_p%20g%20l%20%5Csin%5Ctheta%20%3D%200)

Note that the moment of inertia of the pendulum is considered to be that of a rod pivoted about its end.

![Pendulum moment of inertia](https://latex.codecogs.com/gif.latex?%5CLARGE%20I_p%20%3D%20%5Cfrac%7B1%7D%7B3%7D%20m_p%20l%5E3)

To simulate the system, the fourth-order Runge-Kutta method will be employed. From the equations of motion, <img src="https://render.githubusercontent.com/render/math?math=\ddot%20x"> and <img src="https://render.githubusercontent.com/render/math?math=\ddot%20\theta"> can be isolated to get the following.

![x_ddot](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cddot%7Bx%7D%20%3D%20%5Cfrac%7B%5Cfrac%7B%5Cleft%28%20m_p%20l%20%5Cright%20%29%5E2%20g%20%5Csin%5Ctheta%20%5Ccos%5Ctheta%7D%7BI_p%20&plus;%20m_p%20l%5E2%7D%20-%20m_p%20l%20%5Cdot%7B%5Ctheta%7D%5E2%20%5Csin%5Ctheta%20&plus;%20u%7D%7Bm_c%20&plus;%20m_p%20-%20%5Cfrac%7B%5Cleft%28%20m_p%20l%20%5Ccos%5Ctheta%20%5Cright%20%29%5E2%7D%7BI_p%20&plus;%20m_p%20l%5E2%7D%7D)

![theta_ddot](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cddot%7B%5Ctheta%7D%20%3D%20%5Cfrac%7Bu%20-%20m_p%20l%20%5Cdot%7B%5Ctheta%7D%5E2%20%5Csin%5Ctheta%20&plus;%20%5Cleft%28%20m_c%20&plus;%20m_p%20%5Cright%20%29%20g%20%5Ctan%5Ctheta%7D%7B%5Cfrac%7B%5Cleft%28%20I_p%20&plus;%20m_p%20l%5E2%20%5Cright%29%5Cleft%28%20m_c%20&plus;%20m_p%20%5Cright%20%29%7D%7Bm_p%20l%20%5Ccos%5Ctheta%7D%20-%20m_p%20l%20%5Ccos%5Ctheta%7D)

Consider the following representation of the state of the system.

![State representation](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cvec%7Br%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20x%5C%5C%20v%5C%5C%20%5Ctheta%5C%5C%20%5Comega%20%5Cend%7Bbmatrix%7D)

Lets define a function that relates the derivatives of the state to the original state of the system.

![derivative of state function](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cdot%7B%5Cvec%7Br%7D%7D%20%3D%20f%5Cleft%28%5Cvec%7Br%7D%2C%20t%20%5Cright%20%29%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cdot%7Bx%7D%5C%5C%20%5Cdot%7Bv%7D%5C%5C%20%5Cdot%7B%5Ctheta%7D%5C%5C%20%5Cdot%7B%5Comega%7D%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20v%5C%5C%20%5Cddot%7Bx%7D%5C%5C%20%5Comega%5C%5C%20%5Cddot%7B%5Ctheta%7D%20%5Cend%7Bbmatrix%7D)

The following algorithm is implemented to approximate the state of the system in the following time step from the current state of the system.

![RK4 algorithm equations](https://latex.codecogs.com/gif.latex?%5CLARGE%20k_1%20%3D%20f%28%5Cvec%7Br%7D_i%2C%20t_i%29%5C%5C%5B0.5%20em%5D%20k_2%20%3D%20f%5Cleft%28%20%5Cvec%7Br%7D_i%20&plus;%20%5Cfrac%7Bh%7D%7B2%7Dk_1%2C%20t_i%20&plus;%20%5Cfrac%7Bh%7D%7B2%7D%20%5Cright%20%29%5C%5C%5B0.5%20em%5D%20k_3%20%3D%20f%5Cleft%28%20%5Cvec%7Br%7D_i%20&plus;%20%5Cfrac%7Bh%7D%7B2%7Dk_2%2C%20t_i%20&plus;%20%5Cfrac%7Bh%7D%7B2%7D%20%5Cright%20%29%5C%5C%5B0.5%20em%5D%20k_4%20%3D%20f%5Cleft%28%20%5Cvec%7Br%7D_i%20&plus;%20hk_3%2C%20t_i%20&plus;%20h%20%5Cright%20%29%5C%5C%5B2%20em%5D%20%5Cvec%7Br%7D_%7Bi&plus;1%7D%20%3D%20%5Cvec%7Br%7D_i%20&plus;%20%5Cfrac%7Bh%7D%7B6%7D%20%5Cleft%28%20k_1%20&plus;%202%20k_2%20&plus;%202%20k_3%20&plus;%20k_4%20%5Cright%20%29)

## Implementation

### MainWindow Class

The `MainWindow` class is used to create the GUI that communicates with a `SimulatorWindow` that is used simulate and draw the system. The GUI allows the user to pause and play the simulation, adjust the parameters of the system,  adjust the simulation time step, and specify whether to simulate the system up to some specified end time or to simulate the system indefinitely. 

### SimulatorWindow Class

The `SimulatorWindow` class is responsible for pausing, running, and initializing the simulation with specified parameters based on calls from the `MainWindow` instance.

### RK4Simulator Class

The `RK4Simulator` class is responsible for for performing the simulation by calculating the state of the system in the future based on the current state of the system using the fourth-order Runge-Kutta method.

### DrawSystem Class

The `DrawSystem` class is responsible for drawing the system based on a provided state. 

## Skills Demonstrated

 - Demonstrated strong understanding of numerical methods and ability to apply RK4 algorithm to a system modeled by a set of differential equations.
 - Demonstrated strong understanding of object-oriented programming and familiarity with Python.
	 - Demonstrated understanding of classes and functions and implemented them to compartmentalize the various tasks needed to successfully perform and visualize the simulation.
	 - Demonstrated developing graphical user interfaces with Tkinter.
	 - Implemented multithreading to allow the GUI to be active and usable while also rendering the simulation in the adjacent window.
