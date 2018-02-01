%% The solution sketch for Section 2 of Assignment 1. This file has to be modified and included in the submission.
%% TIP: Maximise the figure window before saving to .png file for better visualization.

clear all;

%% Read .obj files for the object and dice
%%% Read the given meshes using the meshread.m function provided.
object_filename = sprintf('obj_models/vessel.obj');
[obj_v, obj_f, obj_n] = meshread(object_filename);

% Reading dice mesh
[dice_v, dice_f, dice_n] = meshread('obj_models/dice.obj');

%% 1. Read and display meshes in different figures
%%% Read the given meshes using the meshread.m function provided. 
%%% Visualize the two given meshes using the Matlab trisurf function. Assign a random colour to each triangle. 
%%% Save the result of your visualization for each mesh (object and dice) to “1 1.png” and “1 2.png” file, and include these files in your submission.

colours = rand(size(obj_f,2),1);

figure(1);
trisurf(obj_f', obj_v(1,:),  obj_v(2,:), obj_v(3,:), colours)
xlabel('x')
ylabel('y')
zlabel('z')
axis equal

colours1 = rand(size(dice_f,2),1);

figure(2);
trisurf(dice_f', dice_v(1,:),  dice_v(2,:), dice_v(3,:), colours1)
xlabel('x')
ylabel('y')
zlabel('z')
axis equal
%% 2. Apply rotation transformation to object mesh model
%%% Define matrices for rotation of the object around x, y and z axes by 45, 60 and -10 degrees respectively. 
%%% Apply these three transformations to the original (non-transformed) vessel object in the given order 
%%% and visualize the result using trisurf function. 
%%% Save the result of your visualization to "2.png" file and include this file in your submission.

%angles
xa = pi/4;
ya = pi/3;
za = -pi/18;

%x rotation
xr1 = [1; 0; 0];
xr2 = [0; cos(xa); sin(xa)];
xr3 = [0; -sin(xa); cos(xa)];
xr = [xr1 xr2 xr3];

%y rotation
yr1 = [cos(ya); 0; -sin(ya)];
yr2 = [0; 1; 0];
yr3 = [sin(ya); 0; cos(ya)];
yr = [yr1 yr2 yr3];

%z rotation
zr1 = [cos(za);sin(za);0];
zr2 = [-sin(za); cos(za); 0];
zr3 = [0; 0; 1];
zr = [zr1 zr2 zr3];



rotated_object_vertices = zr * (yr * (xr * obj_v));

figure(3);
trisurf(obj_f', rotated_object_vertices(1,:),  rotated_object_vertices(2,:), rotated_object_vertices(3,:), colours);
xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% 3. Apply scaling transformation to object mesh model
%%% Define a matrix for scaling of an object with scaling factor f = [0.5, 2.5, 1.5] in direction of x, y and
%%% z axes. Apply this matrix to your original vessel object (non-transformed) and visualize the result
%%% using trisurf function. Save the result of your visualization to ”3.png” file and include this file in your
%%% submission.

%defining scaling matrix
sc1 = [0.5; 0; 0 0];
sc2 = [0; 2.5; 0 0];
sc3 = [0; 0; 1.5 0];
sc = [sc1 sc2 sc3;
      0 0 0 1];

scaled_object_vertices = sc * obj_v; 


figure(4);
trisurf(obj_f', scaled_object_vertices(1,:), scaled_object_vertices(2,:), scaled_object_vertices(3,:), colours);
xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% 4. Apply translation transformation to object mesh model
%%% Define a matrix for translation of an object by [-200, 500, -100] in direction of x, y and z axes. Apply
%%% this matrix to your original vessel object and visualize the result using trisurf function. Save the result
%%% of your visualization to “4.png” file and include this file in your submission.

%defining translation matrix
tr1 = [-200; 500; -100];
s = size(obj_v);
tr = zeros(s(1), s(2));
tr(1,1:s(2)) = tr1(1,1);
tr(2,1:s(2)) = tr1(2,1);
tr(3,1:s(2)) = tr1(3,1);

translated_object_vertices = plus(tr,obj_v);

trisurf(obj_f', translated_object_vertices(1,:), translated_object_vertices(2,:), translated_object_vertices(3,:), colours);

figure(5);
xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% a) Apply all 4 transformations defined above to your original (non-transformed) vessel object one after the other in the given order.
%% b) Find an appropriate rotation to be applied to the dice mesh so that its top face presents the number 3.
%%% Display both transformed meshes in the same figure using trisurf.
%%% Save the result of your visualisation to "5.png" file and include this file to you submission folder. 
%%% Hint: note that you will need to rotate the dice around an
%%%       appropriate axis (x, y or z) by multiples of 90 degrees.


%% Compute transformations (4x4 transformation matrices)

object_transformation = eye(4); % You will need to compose all previous 4 transformations in homogenous form to find the final transformation of the object
dice_transformation = eye(4); % You will need to find an appropriate rotation represented in homogenous form to bring the dice to the approriate face number

%% Apply object_transformation to all object vertices of vessel

transformed_object_v = obj_v; % TODO (Add your soluton here)

%% Apply dice_transformation transformation to all vertices of the dice

transformed_dice_v = dice_v; % TODO (Add your soluton here)


%% Rendering objects together in the same figure
% Use trisurf to render the objects with random colours
% Tip 1: use 'hold on' to overlay the two objects in the same figure.
%     2: Maximise the figure window before saving to .png file for better visualisation.

figure(6);
%fig1 = trisurf(...)% TODO: plot object and return figure handle
hold on;
%fig2 = trisurf(...)% TODO plot dice and return figure handle (Remember to plot the dice with the correct face)

xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% Submission:
%%% Make required changes to this solution_skeleton.m file and submit it in a zip file along with
%%% the pdf report and the saved figures: "1_1.png", "1_2.png", "2.png", "3.png", "4.png" and "5.png", 
%%%via canvas.
