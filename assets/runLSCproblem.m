addpath schemes
addpath boundary_conditions
addpath lasers
LoadGases  % Loads properties for commonly used gas species

%% Parameter Definition
% Grid settings
chamberLength = 1;  % m, domain axial dimension
chamberRadius = 0.5; % m, domain radial dimension
axialNodes = 101;
radialNodes = 1;

% Time settings
timeStep = 1e-4;  % s
timeEnd = 0.01;  % s

% Initial conditions
chamberPressure = 1e5;  % Pa
flowVelocity = 0.1;  % m s^-1
initialTemperature = 373 .* ones(radialNodes, axialNodes);  % K
initialTemperature(floor(radialNodes/2), floor(axialNodes/2)) = 10000;  % K, set a high-temperature point midway
initialDensity = getDensityFromTemperature(...
    initialTemperature, ...
    chamberPressure, ...
    hydrogenGas);

initialConditions = struct( ...
    "temperature", initialTemperature, ...
    "density", initialDensity, ...
    "velocity", flowVelocity);

%% Setting up LSC Problem with an available numerical solver
problem = LSCProblem(initialConditions, @AxisymmetricFTCS);
problem.setTimeStep(timeStep, timeEnd);
problem.setDomain(chamberLength, axialNodes);
laser = Laser1D(problem, 1e12);  % Use 1D laser model
problem.addLaser(laser);
% problem.addBC();  % Not implemented, boundary conditions assumed constant
problem.solve();