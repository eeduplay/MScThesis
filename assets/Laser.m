classdef Laser < handle
    %Laser: Abstract class definition for laser models
    %   This abstract class provides the template for implementing new laser models

    properties (SetAccess = protected)
        parent
    end

    methods
        function show(obj, timeIndex)
            p = obj.parent;
            imagesc(p.XCoords, p.YCoords, ...
                obj.getIntensity(timeIndex));
            colormap("hot");
            colorbar;
        end
    end

    methods (Abstract)
        I = getIntensity(obj, timeIndex)
    end
end