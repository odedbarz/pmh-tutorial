##############################################################################
#
# Example of particle Metropolis-Hastings in a stochastic volatility model
#
# (c) 2015 Johan Dahlin
# johan.dahlin (at) liu.se
#
##############################################################################

# Import some libraries
import matplotlib.pylab          as plt
import numpy                     as np
import stateEstimationHelper     as helpState
import parameterEstimationHelper as helpParam

# Set the random seed to replicate results in tutorial
np.random.seed( 10 );

##############################################################################
# Define the model
##############################################################################

# Here, we use the following model
#
# x[tt+1] = par[0] * x[tt] + par[1]  * v[tt]
# y[tt]   = par[2] * exp( xt[tt]/2 ) * e[tt]
#
# where v[tt] ~ N(0,1) and e[tt] ~ N(0,1)

# Set the number of time steps
T      = 500;

##############################################################################
# Load data
##############################################################################
y = np.loadtxt('omxs30data.csv')

##############################################################################
# Parameter estimation using PMH
##############################################################################

# The inital guess of the parameter
initPar  = np.array(( 0.99, 0.13, 0.90));

# No. particles in the particle filter ( choose nPart ~ T )
nPart    = 500;

# The length of the burn-in and the no. iterations of PMH ( nBurnIn < nRuns )
nBurnIn  = 2500;
nRuns    = 7500;

# The standard deviation in the random walk proposal
stepSize = np.array(( 0.01, 0.05, 0.05));

# Run the PMH algorithm
res = helpParam.pmh_sv(y,initPar,nPart,T,helpState.pf_sv,nRuns,stepSize)

# State inference
( xhat, ll ) = helpState.pf_sv(y, np.mean( res[nBurnIn:nRuns,:], axis=0 ) ,nPart,T);

#=============================================================================
# Plot the results
#=============================================================================

plt.figure(1);

# Plot the log-returns with volatility estimate
plt.subplot(4,2,(1,2));
plt.plot(y,color = '#1B9E77', linewidth=1.5);
plt.plot(xhat,color = '#D95F02', linewidth=1.5);
plt.xlabel("time"); plt.ylabel("log-return")

# Plot the parameter posterior estimate
# Plot the trace of the Markov chain after burn-in
# Solid black line indicate posterior mean
plt.subplot(4,2,3);
plt.hist(res[nBurnIn:nRuns,0], np.floor(np.sqrt(nRuns-nBurnIn)), normed=1, facecolor='#7570B3')
plt.xlabel("phi"); plt.ylabel("posterior density estimate")
plt.axvline( np.mean(res[nBurnIn:nRuns,0]), linewidth=1.5, color = 'k' )

plt.subplot(4,2,4);
plt.plot(np.arange(nBurnIn,nRuns,1),res[nBurnIn:nRuns,0],color='#7570B3')
plt.xlabel("iteration"); plt.ylabel("trace of phi")
plt.axhline( np.mean(res[nBurnIn:nRuns,0]), linewidth=1.5, color = 'k' )

plt.subplot(4,2,5);
plt.hist(res[nBurnIn:nRuns,1], np.floor(np.sqrt(nRuns-nBurnIn)), normed=1, facecolor='#E7298A')
plt.xlabel("sigmav"); plt.ylabel("posterior density estimate")
plt.axvline( np.mean(res[nBurnIn:nRuns,1]), linewidth=1.5, color = 'k' )

plt.subplot(4,2,6);
plt.plot(np.arange(nBurnIn,nRuns,1),res[nBurnIn:nRuns,1],color='#E7298A')
plt.xlabel("iteration"); plt.ylabel("trace of sigmav")
plt.axhline( np.mean(res[nBurnIn:nRuns,1]), linewidth=1.5, color = 'k' )

plt.subplot(4,2,7);
plt.hist(res[nBurnIn:nRuns,2], np.floor(np.sqrt(nRuns-nBurnIn)), normed=1, facecolor='#66A61E')
plt.xlabel("beta"); plt.ylabel("posterior density estimate")
plt.axvline( np.mean(res[nBurnIn:nRuns,2]), linewidth=1.5, color = 'k' )

plt.subplot(4,2,8);
plt.plot(np.arange(nBurnIn,nRuns,1),res[nBurnIn:nRuns,2],color='#66A61E')
plt.xlabel("iteration"); plt.ylabel("trace of beta")
plt.axhline( np.mean(res[nBurnIn:nRuns,2]), linewidth=1.5, color = 'k' )

##############################################################################
# End of file
##############################################################################