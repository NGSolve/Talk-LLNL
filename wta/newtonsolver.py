from ngsolve import InnerProduct

def NewtonMinimization (a, u):
    w = u.vec.CreateVector()
    r = u.vec.CreateVector()
    uh = u.vec.CreateVector()

    for it in range(10):
        # print("Newton iteration ", it)
        # print ("energy = ", a.Energy(u.vec))
        a.Apply(u.vec, r)
        a.AssembleLinearization(u.vec)
        inv = a.mat.Inverse(u.space.FreeDofs(), inverse="sparsecholesky")
        w.data = inv*r
        err = InnerProduct(w,r)
        if abs(err) < 1e-15: break
        if err < 0:
            # print ("wrong direction")
            w *= -1

        energy = a.Energy(u.vec)
        uh.data = u.vec - w
        tau = 1
        while a.Energy(uh) > energy:
            tau *= 0.5
            # print ("tau = ", tau)
            uh.data = u.vec - tau * w
            # print ("energy uh = ", a.Energy(uh))
        
        u.vec.data = uh

        
