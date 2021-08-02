import numpy as np
import scipy
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.io import loadmat
import numpy.matlib
from scipy.sparse.linalg import eigs
from matplotlib import pyplot as plt

# load the dataset from a provided .mat file, re-center it around the origin and return it as a NumPy array of floats
def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea']
    x = np.array(x)
    # the number of images we're analyzing
    # n = len(x)
    # d, the dimension of those images
    # d = len(x[0])
    np.mean(x, axis=0)
    x = x - np.mean(x, axis=0)
    return x


# calculate and return the covariance matrix of the dataset as a NumPy matrix (d x d array)
def get_covariance(dataset):
    x = dataset
    t = np.transpose(x)
    s = np.dot(t, x) / (len(x) - 1)
    return s


# perform eigen decomposition on the covariance matrix S and return a diagonal matrix (NumPy array) with the
# largest m eigenvalues on the diagonal, and a matrix (NumPy array) with the corresponding eigenvectors as columns
def get_eig(S, m):
    f, vec = scipy.linalg.eigh(S, eigvals=(len(S) - m, len(S) - 1))
    vec = np.fliplr(vec)
    f = np.flipud(f)
    d = np.diag(f)
    return d, vec

# project each image into your m-dimensional space and return the new representation as a d x 1 NumPy array
def project_image(image, U):
    d=len(U[0])
    project=numpy.zeros(shape=np.dot(np.dot(np.transpose(U[:, 0]), image), U[:, 0]).shape)
    #print(project)
    for i in range(d):
        a = np.dot(np.transpose(U[:, i]), image)
        p = np.dot(a, U[:, i])
        project = project + p
    return project

# use matplotlib to display a visual representation of the original image and the projected image side-by-side
def display_image(orig, proj):
    orig=np.transpose(numpy.reshape(orig,(32,32,)))
    proj = np.transpose(numpy.reshape(proj, (32, 32,)))
    fig, (ax1,ax2) = plt.subplots(1, 2)
    ax1.set_title('Original')
    pos0=ax1.imshow(orig, aspect='equal')
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(pos0, cax=cax)

    ax2.set_title('Projection')
    pos1=ax2.imshow(proj, aspect='equal')
    divider2 = make_axes_locatable(ax2)
    cax2 = divider2.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(pos1,cax=cax2)
    plt.show()
