'''
Created on Aug 17, 2010

@author: Peter Harrington
peter.b.harrington@gmail.com
'''
from numpy import *

def cadf(inMatX, inMatY, p, nlags):
    if (p < -1):
        print ("Error: p cannot be less than -1")
    numObs = inMatX.shape[0]
    if ((numObs - 2*nlags + 1) < 1):
        print ("Error nlags is too large in cadf, negative degrees of freedom")
        
    inMatX = detrend(inMatX,p)
    inMatY = detrend(inMatY,p)
    b = ((inMatX.transpose()*inMatX).I)*(inMatX.transpose()*inMatY)
    r = inMatY - inMatX*b
    dep = tdiff(r,1)
    dep = trimr(dep,1,0)
    z = trimr(lag(r,1),1,0)
    k = 1
    while (k <= nlags):
        z = concatenate((z,lag(dep,k)),1)
        k += 1
    z = trimr(z,nlags,0)
    dep = trimr(dep,nlags,0)
    
    dtemp = detrend(z,0)
    beta = linalg.solve(dtemp.transpose()*dtemp, dtemp.transpose()*detrend(dep,0))    #beta = a\b
    res = detrend(dep,0) - detrend(z,0)*beta
    so = (res.transpose()*res)/(dep.shape[0]-z.shape[1])
    var_cov = so[0,0] * ((z.transpose()*z).I)
    
    results={}          #use dictonary to return bundled results
    results['alpha'] = beta[0,0]
    results['adf'] = beta[0,0]/sqrt(var_cov[0,0])
    results['crit'] = rztcrit(numObs,inMatX.shape[1],p)
    results['nlag'] = nlags
    results['nvar'] = inMatX.shape[1]   #number of columns in inMatX
    return results
    
def detrend(inputMatrix, p):
    if p == -1:
        return inputMatrix
    
    numObs = inputMatrix.shape[0]
    u = matrix(ones((numObs,1)))                #create 0th order term
    
    if (p > 0): #create a time matrix
        timep = matrix(zeros((numObs,p)))
        t = matrix(range(numObs))
        tp = t.transpose()/float(numObs)
        m = 1
        while (m <= p):
            timep[:,m-1] = multiply(tp,m)
            m += 1
        xmat = concatenate((u,timep),1)
    else:
        xmat = u
    xpxi = (xmat.transpose()*xmat).I            #denom for ols
    beta = xpxi*(xmat.transpose()*inputMatrix)  #calc ols
    residuals = inputMatrix - xmat*beta         #subtract residuals
    return residuals

def lag(inMatX, n = 1, v = 0):
    zt = multiply(matrix(ones((n,inMatX.shape[1]))),v) #zero term
    z = concatenate((zt,trimr(inMatX,0,n)))
    return z

def tdiff(inputMatrix, k):
    numObs,numVar = inputMatrix.shape
    if k==0:
        dmat = inputMatrix
    elif k == 1:
        dmat = matrix(zeros((numObs,numVar)))
        dmat[1:numObs,:] = inputMatrix[1:numObs,:]-inputMatrix[0:numObs-1,:]
    else:
        dmat = matrix(zeros((numObs,numVar)))
        dmat[k:numObs,:] = inputMatrix[k:numObs,:]-inputMatrix[0:numObs-k,:]
    return dmat

def trimr(inputMatrix, bottom, top):
    n = inputMatrix.shape[0]
    return inputMatrix[bottom:n-top,:]

def rztcrit(numObs,k,p):
    if (numObs >= 500):
        zt = matrix('\
-3.28608,-2.71123,-2.44427,-0.22827,0.19684,1.07845;\
-3.88031,-3.35851,-3.03798,-1.01144,-0.65334,0.15312;\
-4.36339,-3.84931,-3.52926,-1.59069,-1.27691,-0.68855;\
-4.69226,-4.16473,-3.91069,-2.03499,-1.75167,-1.16909;\
-5.12583,-4.55603,-4.24350,-2.43062,-2.15918,-1.63241;\
-5.45902,-4.85433,-4.54552,-2.68999,-2.45059,-1.96213;\
-5.68874,-5.13084,-4.85451,-3.01287,-2.77470,-2.34774;\
-3.95399,-3.33181,-3.01057,-0.96426,-0.63214,0.14815;\
-4.29147,-3.77581,-3.47606,-1.47435,-1.15649,-0.38209;\
-4.80216,-4.16163,-3.87422,-1.95661,-1.68975,-1.17624;\
-5.08973,-4.49148,-4.22534,-2.34763,-2.09506,-1.52368;\
-5.28946,-4.77944,-4.49057,-2.63483,-2.39227,-1.88262;\
-5.64107,-5.10086,-4.81771,-2.95313,-2.74233,-2.30293;\
-5.84555,-5.26853,-5.01340,-3.21419,-2.95790,-2.50159;\
-4.25439,-3.69759,-3.42840,-1.49852,-1.22694,-0.59376;\
-4.62332,-4.12603,-3.83833,-1.91632,-1.65271,-0.93775;\
-5.09990,-4.50073,-4.18896,-2.26553,-1.97459,-1.41616;\
-5.23982,-4.74879,-4.50065,-2.59004,-2.30601,-1.76624;\
-5.63745,-5.07700,-4.77794,-2.88029,-2.66305,-2.25529;\
-5.87733,-5.31763,-5.03729,-3.17526,-2.94043,-2.54329;\
-6.08463,-5.57014,-5.29279,-3.45890,-3.21035,-2.68331;\
-4.68825,-4.14264,-3.83668,-1.89022,-1.62543,-1.02171;\
-5.00664,-4.43544,-4.14709,-2.24334,-1.94304,-1.29258;\
-5.42102,-4.77343,-4.48998,-2.57209,-2.30366,-1.79885;\
-5.60249,-5.02686,-4.77574,-2.89195,-2.61726,-2.09253;\
-5.90744,-5.31272,-5.04121,-3.16076,-2.89667,-2.44274;\
-6.16639,-5.58218,-5.28049,-3.40263,-3.15765,-2.70251;\
-6.29638,-5.79252,-5.52324,-3.65372,-3.40115,-2.94514;\
-4.99327,-4.43088,-4.13314,-2.19577,-1.94806,-1.33955;\
-5.28724,-4.72773,-4.46224,-2.52556,-2.25121,-1.75592;\
-5.53603,-5.03231,-4.74442,-2.81101,-2.53978,-2.01464;\
-5.85790,-5.28516,-4.99765,-3.11650,-2.85684,-2.38643;\
-6.03218,-5.50167,-5.24244,-3.37898,-3.13182,-2.57977;\
-6.38137,-5.80056,-5.52693,-3.62856,-3.37482,-2.85511;\
-6.60394,-6.03056,-5.73651,-3.83174,-3.56048,-3.09560')
    elif ((numObs >= 400) and (numObs <= 499)):
        zt = matrix('\
-3.39320,-2.78062,-2.47410,-0.27917,0.17257,1.01757;\
-3.81898,-3.34274,-3.04197,-0.98464,-0.63219,0.07862;\
-4.43824,-3.83476,-3.53856,-1.59769,-1.32538,-0.68273;\
-4.78731,-4.19879,-3.90468,-2.03620,-1.78519,-1.25540;\
-5.15859,-4.55815,-4.27559,-2.40402,-2.15148,-1.64991;\
-5.36666,-4.82211,-4.55480,-2.73039,-2.47586,-1.96342;\
-5.70533,-5.14149,-4.83768,-2.98968,-2.75467,-2.33244;\
-3.88099,-3.31554,-3.00918,-1.01400,-0.66651,0.11221;\
-4.35920,-3.76677,-3.47891,-1.47887,-1.17461,-0.45761;\
-4.73655,-4.17175,-3.87843,-1.95622,-1.67273,-1.05752;\
-5.03407,-4.48465,-4.18736,-2.32047,-2.06844,-1.54620;\
-5.37301,-4.80609,-4.50790,-2.65816,-2.39100,-1.90516;\
-5.63842,-5.08273,-4.79419,-2.95211,-2.72047,-2.26114;\
-5.95823,-5.38482,-5.08735,-3.23862,-2.98661,-2.58060;\
-4.29209,-3.74752,-3.44785,-1.49664,-1.19363,-0.54054;\
-4.73620,-4.16373,-3.83159,-1.87826,-1.56786,-0.90630;\
-4.98331,-4.47817,-4.18238,-2.27544,-1.99733,-1.45956;\
-5.34322,-4.77455,-4.47877,-2.60581,-2.34669,-1.82075;\
-5.61331,-5.05800,-4.77543,-2.91228,-2.64829,-2.13015;\
-5.94606,-5.34094,-5.05669,-3.17314,-2.92833,-2.50131;\
-6.17994,-5.62560,-5.32022,-3.45919,-3.21928,-2.73838;\
-4.68326,-4.13893,-3.83504,-1.88594,-1.59783,-1.02900;\
-5.01959,-4.44111,-4.16075,-2.24225,-1.96550,-1.36753;\
-5.35312,-4.76318,-4.48253,-2.53350,-2.26862,-1.74966;\
-5.65846,-5.05443,-4.74318,-2.86021,-2.61633,-2.15096;\
-5.89297,-5.33097,-5.03686,-3.13780,-2.88399,-2.36895;\
-6.11791,-5.59035,-5.29834,-3.39283,-3.13194,-2.64558;\
-6.43463,-5.83831,-5.54375,-3.63526,-3.40822,-2.97731;\
-4.99049,-4.45174,-4.15603,-2.22388,-1.94107,-1.40933;\
-5.37057,-4.77929,-4.48921,-2.54431,-2.27297,-1.72675;\
-5.61805,-5.06136,-4.76461,-2.81651,-2.54785,-2.04956;\
-5.88425,-5.29788,-5.01558,-3.10698,-2.83781,-2.33035;\
-6.15156,-5.57259,-5.28198,-3.36062,-3.10140,-2.61065;\
-6.37314,-5.80031,-5.51577,-3.63686,-3.38505,-2.87176;\
-6.58251,-6.03057,-5.74573,-3.85037,-3.60485,-3.11932')
    elif ((numObs >= 300) and (numObs <= 399)):
        zt = matrix('\
-3.36203,-2.77548,-2.46139,-0.28681,0.13287,1.03471;\
-3.90239,-3.32711,-3.03723,-0.99653,-0.60551,0.11851;\
-4.32982,-3.81156,-3.51879,-1.59453,-1.29025,-0.57675;\
-4.81264,-4.24058,-3.93314,-2.05226,-1.79734,-1.23867;\
-5.09929,-4.53317,-4.26022,-2.39047,-2.15062,-1.66121;\
-5.40020,-4.84728,-4.56541,-2.72073,-2.48276,-2.01238;\
-5.72554,-5.14543,-4.85290,-3.03642,-2.79747,-2.38877;\
-3.93064,-3.31039,-3.00695,-1.02551,-0.69206,0.10488;\
-4.30844,-3.76971,-3.48291,-1.49867,-1.18293,-0.44930;\
-4.69802,-4.16002,-3.85937,-1.95172,-1.66941,-1.07873;\
-5.09621,-4.51913,-4.22178,-2.32005,-2.06940,-1.52440;\
-5.39988,-4.84499,-4.54918,-2.66241,-2.40886,-1.94518;\
-5.67194,-5.12143,-4.83266,-2.95787,-2.71575,-2.26783;\
-5.90971,-5.38093,-5.10006,-3.24590,-3.00999,-2.55590;\
-4.32518,-3.77645,-3.46220,-1.48724,-1.19931,-0.53182;\
-4.66166,-4.12423,-3.82665,-1.85992,-1.56770,-0.95256;\
-5.06263,-4.47715,-4.19478,-2.27228,-1.98935,-1.40857;\
-5.39577,-4.79037,-4.51644,-2.60186,-2.32067,-1.82448;\
-5.62591,-5.09997,-4.78451,-2.89543,-2.66108,-2.16281;\
-5.96117,-5.38487,-5.08529,-3.19176,-2.95677,-2.45750;\
-6.18044,-5.61962,-5.32402,-3.44453,-3.18600,-2.75024;\
-4.69949,-4.11581,-3.84809,-1.91652,-1.63097,-1.06354;\
-5.02878,-4.48050,-4.18169,-2.20023,-1.92196,-1.37122;\
-5.37891,-4.82102,-4.49501,-2.55100,-2.29407,-1.76313;\
-5.59926,-5.07560,-4.78056,-2.89047,-2.61834,-2.11372;\
-5.97404,-5.35040,-5.03148,-3.15838,-2.91666,-2.44570;\
-6.20250,-5.64756,-5.33112,-3.40255,-3.16800,-2.73795;\
-6.40258,-5.84695,-5.58164,-3.67811,-3.42766,-2.97315;\
-5.02873,-4.44103,-4.15164,-2.19792,-1.94100,-1.39467;\
-5.36834,-4.76996,-4.46992,-2.53666,-2.27257,-1.73355;\
-5.59537,-5.05016,-4.78520,-2.83093,-2.57279,-2.07503;\
-5.85590,-5.33224,-5.03207,-3.11489,-2.86007,-2.36551;\
-6.20771,-5.62475,-5.32273,-3.36439,-3.10806,-2.63899;\
-6.38397,-5.87287,-5.56819,-3.63376,-3.37917,-2.87215;\
-6.69353,-6.08474,-5.78590,-3.87231,-3.61022,-3.14908')
    elif ((numObs >= 200) and (numObs <= 299)):
        zt = matrix('\
-3.35671,-2.77519,-2.46594,-0.25410,0.19613,1.07222;\
-3.92428,-3.38037,-3.08215,-1.00759,-0.63422,0.09456;\
-4.48168,-3.83395,-3.54540,-1.60205,-1.31840,-0.73432;\
-4.82954,-4.23468,-3.94803,-2.05472,-1.80434,-1.27245;\
-5.19748,-4.57984,-4.28594,-2.42219,-2.18483,-1.73071;\
-5.48348,-4.89872,-4.60436,-2.75423,-2.51959,-2.06231;\
-5.82241,-5.21284,-4.90675,-3.03145,-2.79112,-2.38818;\
-3.88242,-3.33232,-3.01999,-0.98826,-0.63342,0.12132;\
-4.36630,-3.76414,-3.46091,-1.48625,-1.15077,-0.49842;\
-4.76842,-4.20038,-3.89975,-1.93433,-1.63407,-1.04290;\
-5.05007,-4.54203,-4.23534,-2.35721,-2.10330,-1.57965;\
-5.46384,-4.89647,-4.60567,-2.66674,-2.41227,-1.92884;\
-5.80068,-5.17731,-4.86360,-2.97354,-2.71548,-2.25152;\
-6.01552,-5.48792,-5.18651,-3.27732,-3.05193,-2.62313;\
-4.37038,-3.77348,-3.48123,-1.46468,-1.19712,-0.52291;\
-4.71164,-4.17296,-3.87214,-1.88824,-1.61792,-0.99897;\
-5.07287,-4.49791,-4.19539,-2.25537,-1.97775,-1.42073;\
-5.43158,-4.85660,-4.55542,-2.59513,-2.34448,-1.88253;\
-5.71928,-5.15509,-4.85008,-2.91869,-2.67892,-2.16537;\
-5.95901,-5.38920,-5.10190,-3.21921,-2.97088,-2.49105;\
-6.24842,-5.69150,-5.39236,-3.47876,-3.22814,-2.81954;\
-4.76132,-4.12120,-3.81887,-1.87640,-1.57988,-0.95925;\
-5.07595,-4.49599,-4.18062,-2.22181,-1.95429,-1.32816;\
-5.41865,-4.82420,-4.51442,-2.54584,-2.28898,-1.71129;\
-5.69988,-5.10837,-4.81872,-2.87861,-2.62537,-2.10745;\
-6.03815,-5.41121,-5.11067,-3.15726,-2.89572,-2.39236;\
-6.31746,-5.67322,-5.35729,-3.42445,-3.18255,-2.72287;\
-6.54722,-5.92036,-5.63475,-3.68619,-3.44087,-2.99590;\
-5.06954,-4.48980,-4.16461,-2.22770,-1.95682,-1.39685;\
-5.35737,-4.81634,-4.52940,-2.54416,-2.26355,-1.73669;\
-5.65024,-5.06222,-4.78444,-2.84019,-2.55801,-2.03438;\
-6.01717,-5.38593,-5.07183,-3.10854,-2.83015,-2.38316;\
-6.22810,-5.62644,-5.32983,-3.37920,-3.11022,-2.58412;\
-6.51923,-5.91250,-5.61917,-3.64604,-3.37807,-2.91979;\
-6.74433,-6.15641,-5.85483,-3.88559,-3.62884,-3.22791')
    elif ((numObs >= 1) and (numObs <= 199)):
        zt = matrix('\
-3.40026,-2.81980,-2.49012,-0.28406,0.16278,0.99118;\
-4.02456,-3.40397,-3.08903,-0.99877,-0.63826,0.09294;\
-4.50406,-3.91574,-3.60618,-1.64640,-1.34126,-0.67499;\
-4.97750,-4.31424,-4.00116,-2.07039,-1.80758,-1.24622;\
-5.29795,-4.65255,-4.36236,-2.43756,-2.20744,-1.74384;\
-5.69006,-5.02821,-4.70153,-2.78533,-2.55054,-2.12221;\
-6.01114,-5.32900,-5.01614,-3.10458,-2.87108,-2.45944;\
-4.03875,-3.38465,-3.06445,-1.01452,-0.67017,0.08305;\
-4.49697,-3.83781,-3.52924,-1.50657,-1.18131,-0.49457;\
-4.85358,-4.24290,-3.92668,-1.93268,-1.67668,-1.11969;\
-5.23415,-4.63779,-4.32076,-2.35203,-2.10299,-1.58236;\
-5.60428,-4.99996,-4.67591,-2.71512,-2.45663,-1.97999;\
-5.89816,-5.30839,-4.98307,-3.01998,-2.78403,-2.33971;\
-6.24667,-5.61312,-5.28841,-3.32373,-3.07681,-2.65243;\
-4.50725,-3.84730,-3.53859,-1.50198,-1.21063,-0.49494;\
-4.87844,-4.22489,-3.92431,-1.88702,-1.59187,-0.97217;\
-5.20113,-4.56724,-4.27167,-2.29534,-2.03226,-1.43479;\
-5.61984,-4.95138,-4.63381,-2.62062,-2.34903,-1.81713;\
-5.93516,-5.26326,-4.95702,-2.97158,-2.70668,-2.22094;\
-6.20848,-5.57967,-5.28403,-3.27115,-3.01521,-2.58367;\
-6.52806,-5.84919,-5.55596,-3.54144,-3.30790,-2.88872;\
-4.84291,-4.21809,-3.89360,-1.88296,-1.62337,-0.99875;\
-5.18976,-4.56495,-4.23781,-2.23973,-1.95745,-1.36282;\
-5.49570,-4.91049,-4.57949,-2.54844,-2.30040,-1.81108;\
-5.85200,-5.24753,-4.90738,-2.89515,-2.62635,-2.11513;\
-6.25788,-5.59734,-5.23154,-3.20543,-2.95304,-2.49876;\
-6.42744,-5.80415,-5.49459,-3.46836,-3.20457,-2.78454;\
-6.79276,-6.11558,-5.77461,-3.74987,-3.49703,-3.07378;\
-5.25985,-4.56675,-4.25742,-2.24159,-1.93760,-1.40055;\
-5.53963,-4.88523,-4.55008,-2.53159,-2.26558,-1.74469;\
-5.86277,-5.23537,-4.92559,-2.84160,-2.58154,-2.08171;\
-6.16676,-5.52360,-5.22425,-3.12455,-2.84785,-2.41246;\
-6.43205,-5.80308,-5.46594,-3.42417,-3.19918,-2.69791;\
-6.81177,-6.11377,-5.74083,-3.67826,-3.41996,-2.95145;\
-6.98960,-6.36882,-6.03754,-3.95573,-3.71192,-3.30766')
    if ((k < 1) or (k > 5) or (p > 5)):
        crit = matrix(zeros((6,1)))
    n = (k - 1) * 7 + p + 2
    crit = zt[n-1,:]
    return crit
