function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples
rtheta = [0; theta(2:length(theta))];

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%
h = (X * theta) - y;
L = (rtheta' * rtheta) * (lambda / (2 * m));
J = ((h' * h) / (2 * m)) + L;
R = (rtheta' .* (lambda / m));
G = (h' * (X / m)) + R;

% =========================================================================

grad = G(:);

end
