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
xr1 = [1; 0; 0; 0];
xr2 = [0; cos(xa); sin(xa); 0];
xr3 = [0; -sin(xa); cos(xa); 0];
xr4 = [0; 0; 0; 1];
xr = [xr1 xr2 xr3 xr4];


%y rotation
yr1 = [cos(ya); 0; -sin(ya); 0];
yr2 = [0; 1; 0; 0];
yr3 = [sin(ya); 0; cos(ya); 0];
yr4 = [0; 0; 0; 1]
yr = [yr1 yr2 yr3 yr4];

%z rotation
zr1 = [cos(za);sin(za);0; 0];
zr2 = [-sin(za); cos(za); 0; 0];
zr3 = [0; 0; 1; 0];
zr4 = [0; 0; 0; 1];
zr = [zr1 zr2 zr3 zr4];

r = zr * yr * xr;

s = size(obj_v,2);
rotated_object_vertices = r * [obj_v; ones(1,s)];


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

%defining the scaling matrix:
sc1 = [0.5; 0; 0; 0];
sc2 = [0; 2.5; 0; 0];
sc3 = [0; 0; 1.5 ;0];
sc4 = [0; 0; 0; 1];
sc = [sc1, sc2, sc3, sc4];


scaled_object_vertices = sc * [obj_v; ones(1,s)];



figure(4);
trisurf(obj_f',scaled_object_vertices(1,:), scaled_object_vertices(2,:), scaled_object_vertices(3,:), colours);
xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% 4. Apply translation transformation to object mesh model
%%% Define a matrix for translation of an object by [-200, 500, -100] in direction of x, y and z axes. Apply
%%% this matrix to your original vessel object and visualize the result using trisurf function. Save the result
%%% of your visualization to “4.png” file and include this file in your submission.

%definining translation matrix
tr1 = [1; 0; 0; 0];
tr2 = [0; 1; 0 ;0];
tr3 = [0; 0; 1; 0];
tr4 = [-200; 500; -100; 1];
tr = [tr1 tr2 tr3 tr4];


translated_object_vertices = tr * [obj_v; ones(1,s)];

figure(5);
trisurf(obj_f',translated_object_vertices(1,:), translated_object_vertices(2,:), translated_object_vertices(3,:), colours);

xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% a) Apply all 3 transformations defined above to your original (non-transformed) vessel object one after the other in the given order.zall_trans_obj_vertices = al

%% b) Find an appropriate rotation to be applied to the dice mesh so that its top face presents the number 3.
%%% Display both transformed meshes in the same figure using trisurf.
%%% Save the result of your visualisation to "5.png" file and include this file to you submission folder. 
%%% Hint: note that you will need to rotate the dice around an
%%%       appropriate axis (x, y or z) by multiples of 90 degrees.


%angles
xa = 0;
ya = -pi/2;
za = 0;


%x rotation
xr1 = [1; 0; 0; 0];
xr2 = [0; cos(xa); sin(xa); 0];
xr3 = [0; -sin(xa); cos(xa); 0];
xr4 = [0; 0; 0; 1];
xr2 = [xr1 xr2 xr3 xr4];


%y rotation
yr1 = [cos(ya); 0; -sin(ya); 0];
yr2 = [0; 1; 0; 0];
yr3 = [sin(ya); 0; cos(ya); 0];
yr4 = [0; 0; 0; 1]
yr2 = [yr1 yr2 yr3 yr3];

%z rotation
zr1 = [cos(za);sin(za);0; 0];
zr2 = [-sin(za); cos(za); 0; 0];
zr3 = [0; 0; 1; 0];
zr4 = [0; 0; 0; 1];
zr2 = [zr1 zr2 zr3 zr4];


%% Compute transformations (4x4 transformation matrices)

object_transformation = tr * sc * r;
dice_transformation = yr2;

%% Apply object_transformation to all object vertices of vessel

transformed_object_v = object_transformation * [obj_v; ones(1,s)]

%% Apply dice_transformation transformation to all vertices of the dice

ds = size(dice_v, 2);
transformed_dice_v = dice_transformation * [dice_v; ones(1,ds)];


%% Rendering objects together in the same figure
% Use trisurf to render the objects with random colours
% Tip 1: use 'hold on' to overlay the two objects in the same figure.
%     2: Maximise the figure window before saving to .png file for better visualisation.
 


figure(6);
trisurf(obj_f',transformed_object_v(1,:), transformed_object_v(2,:), transformed_object_v(3,:), colours);
hold on;
trisurf(dice_f',transformed_dice_v(1,:), transformed_dice_v(2,:), transformed_dice_v(3,:), colours1);

xlabel('x')
ylabel('y')
zlabel('z')
axis equal

%% Submission:
%%% Make required changes to this solution_skeleton.m file and submit it in a zip file along with
%%% the pdf report and the saved figures: "1_1.png", "1_2.png", "2.png", "3.png", "4.png" and "5.png", via canvas.