## Inventory Optimization code


This repo contains code that solves "Inventory optimization problem". 



Install the environment first:

     pipenv install -r requirements.txt

Run tests:

     pytest

Below we have written the optimization objective and constraints.

$$\begin{aligned}
\underset{x}{\text{minimize}}\quad &\sum_{i}^{N}\sum_{j}^{M}\sum_{k}^{K}x_{i,j,k}*n_{k}*shipping_{i,j} + \sum_{i}^{N}\sum_{r}^{R}y_{i,r}*procurement_{i,r}\\
\text{subject to}\quad &\\
& \sum_{i}^{N}x_{i,j,k}\geq d_{j,k}, \quad \forall (j,k) \\
& \sum_{j}^{N}\sum_{k’}x_{i,j,k’}*n_{k’,r} - q_{i,r} \leq y_{i,r}\quad \forall r,i \\
& q_{i,r} - \sum_{j}^{M}\sum_{k’}x_{i,j,k’}*n_{k’,r}\leq v_{i,r}\quad \forall r,i \\
& \sum_{j}^{N}\sum_{k}^{K}x_{i,j,k}*n_{k}+\sum_{r}^{R}v_{i,r}\leq capacity_{i}\quad \forall i \\
& x_{i,j,k}\quad, \quad y_{i,r}\quad, \quad v_{i,r} \in \mathbb{W}
\end{aligned}$$

$x_{i,j,k}$ - decision variable, stand for number of product sets k that will be delivered from warehouse i to store j\
$y_{i,r}$- decision variable, stands for number of procurement skus r in distributive center i\
$v_{i,r}$- variables that represent number of unused skus r that is going to left stored in warehouse i\
$capacity_{i}$- capacity of wearhouse i\
$shipping_{i,j}$- cost of shipping sku unit from wearhouse i to warehouse j\
$procurement_{i,r}$- cost of procurement of sku r in warehouse i\
$d_{j,k}$- demand of product sets k in store j\
$q_{i,r}$- current quantity of sku r in warehouse i\
$n_{k,r}$- total number of sku r in product sets k\
$i$- index of warehouse\
$j$ - index of store\
$k$- index of product set\
$r$- index of sku\

## License

```
Copyright 2022 Grid Dynamics International, Inc. All Rights Reserved

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Authors

- Marko Nikolic, `mnikolic@griddynamics.com`
- Dejan Dzunja, `ddzunja@griddynamics.com`
- Andriy Drebot, `adrebot@griddynamics.com`
