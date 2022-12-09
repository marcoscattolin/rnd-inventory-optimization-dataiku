## Inventory Optimization code


This repo contains code that solves "Inventory optimization problem". 



Install the environment first:

     pipenv install -r requirements.txt

Run tests:

     pytest

Below we have written the optimization objective and constraints.

$$\text{min}\sum_i\sum_j\sum_k x_{i,j,k} \cdot n_k \cdot shipping_{i,j} + \sum_i \sum_r y_{i,r} \cdot procurement_{i,r}$$

constraint:

$$\sum_{i} z_{i,j,k} = 1 \;\;\; \forall(j, k)$$

$$z_{i,j,k} \cdot d_{j, k} \leq x_{i,j,k} \;\;\; \forall(i, j, k)$$

$$\sum_j\sum_{k'}x_{i, j, k'} - q_{i ,r} \leq y_{i, r} \;\;\; \forall(i, r)$$

$$q_{i ,r}  - \sum_j\sum_{k'}x_{i, j, k'} \leq v_{i, r} \;\;\; \forall(i, r)$$

$$\sum_j\sum_{k'}x_{i, j, k'} \cdot n_k + \sum_r v_{i,r} \leq capacity_i \;\; \forall i$$


$z_{i,j,k} \in [0, 1]$
$x_{i,j,k} \in \mathbb{N_0}$,
$y_{i,r} \in \mathbb{N_0}$,
$v_{i,r} \in \mathbb{N_0}$
