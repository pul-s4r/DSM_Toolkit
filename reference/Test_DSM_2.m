% **************************************************************************
% **************************************************************************
% **************************************************************************
% **************************************************************************
% **************************************************************************
%																									*
%  Files:	Test_DSM_1.m																	*
%																									*
%	Created by: Ronnie E. Thebeau															*
%					System Design and Management Program								*
%					Massacusetts Institute of Technology								*
%																									*
%	Date: December 2000																		*
%																									*
% Entries indicate an interaction between two elements and the value 		*
% represents the interaction strength													*
%																									*
% This DSM represents a subset of elements and interactions	within a			*
% generic elevator system																	*
%																									*
% **************************************************************************
% **************************************************************************
% **************************************************************************
% **************************************************************************




% **************************************************************************
%								DSM TEMPLATE													*
% **************************************************************************

DSM_size = 8;				% number of elements in the DSM
DSM = zeros(DSM_size);

% ***** DSM ENTRIES *****

DSM( 1,  1) = 1;
DSM( 2,  1) = 1; 
DSM( 3,  1) = 1; 
DSM( 4,  1) = 1; 

DSM( 2,  2) = 1;
DSM( 1,  2) = 1;
DSM( 3,  2) = 1;
DSM( 4,  2) = 1;

DSM( 3,  3) = 1; 
DSM( 1,  3) = 1; 
DSM( 5,  3) = 1; 

DSM( 4,  4) = 1; 
DSM( 5,  4) = 1; 
DSM( 6,  4) = 1; 

DSM( 5,  5) = 1; 
DSM( 7,  5) = 1; 

DSM( 6,  6) = 1; 
DSM( 7,  6) = 1; 

DSM( 7,  7) = 1; 
DSM( 4,  7) = 1; 
DSM( 8,  7) = 1; 


DSM( 8,  8) = 1; 

% **************************************************************************
%									DSM Elements Labels										*
% **************************************************************************

DSMLABEL = cell(DSM_size,1);

DSMLABEL{1,1} = 'A';
DSMLABEL{2,1} = 'B';
DSMLABEL{3,1} = 'C';
DSMLABEL{4,1} = 'D';
DSMLABEL{5,1} = 'E';
DSMLABEL{6,1} = 'F';
DSMLABEL{7,1} = 'G';
DSMLABEL{8,1} = 'H';


% **************************************************************************
%					Functional Mapping to Physical Elements							*
% **************************************************************************

% Each of the functional labels represents the functional 
% requirement for which the physcial DSM element represents
% Used to cross-reference the physical elemnts and
% functional requiremnts

