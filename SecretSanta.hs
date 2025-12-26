{-# LANGUAGE RecordWildCards #-}

module SecretSanta
  ( secretSanta      -- pure generator, given an RNG
  , secretSantaIO    -- convenience wrapper using StdGen from IO
  ) where

import System.Random (RandomGen, StdGen, getStdGen, uniformR)
import Data.List (delete)

-- State threaded purely through recursion
data DeriveState = DeriveState
  { people      :: [Int]           -- 1..n
  , givers      :: [Int]           -- not yet chosen as current giver
  , recipients  :: [Int]           -- can be chosen as recipient
  , assignments :: [(Int, Int)]    -- (giver, recipient), built backwards
  } deriving Show

-- Pick a random element from a non-empty list, returning element and new RNG
pick :: RandomGen g => [a] -> g -> (a, g)
pick xs g =
  let (i, g') = uniformR (0, length xs - 1) g
  in  (xs !! i, g')

-- Pure algorithm: single pass, two pools, no fixed points, multiple cycles.
-- Returns (assignments, newRng). The caller is responsible for providing the RNG.
secretSanta :: RandomGen g => Int -> g -> ([(Int, Int)], g)
secretSanta n g0
  | n < 2     = error "n must be greater than 1"
  | otherwise =
      let ps = [1 .. n]
          -- choose initial giver and apply 1': remove from givers
          (firstGiver, g1) = pick ps g0
          st0 = DeriveState
            { people      = ps
            , givers      = delete firstGiver ps   -- step 1'
            , recipients  = ps
            , assignments = []
            }
      in  run firstGiver g1 st0
  where
    run :: RandomGen g => Int -> g -> DeriveState -> ([(Int, Int)], g)
    run currentGiver g st@DeriveState{..}
      -- Termination: all recipients used, so everyone has received exactly once
      | null recipients =
          (reverse assignments, g)

      | otherwise =
          let -- candidates: recipients except currentGiver
              candidates = filter (/= currentGiver) recipients
          in
          case candidates of
            [] ->
              -- Under the described rules this should not occur:
              -- if it does, there is a logical error in the invariant.
              error "SecretSanta: reached impossible state (no valid recipient)"

            _  ->
              let -- choose recipient for currentGiver
                  (recipient, g') = pick candidates g

                  -- update recipient pool: remove chosen recipient;
                  -- currentGiver is not reinserted as a recipient, because
                  -- in this model nobody is ever their own recipient and each
                  -- person will eventually appear exactly once as a recipient.
                  newRecipients  = delete recipient recipients

                  newAssignments = (currentGiver, recipient) : assignments
              in
              if null givers
                then
                  -- No unused givers left. Since recipients is non-empty here,
                  -- exactly one giver and one recipient remain to be matched.
                  -- The invariant "candidate list excludes currentGiver" plus
                  -- the fact we just chose 'recipient' from candidates ensures
                  -- currentGiver /= recipient, so the last pair is valid and
                  -- no extra step is needed: the recursion will end next time.
                  run currentGiver g' st
                    { recipients  = newRecipients
                    , assignments = newAssignments
                    }
                else
                  -- Step 5 + step 1': choose next giver and remove from givers
                  let (nextGiver, g'') = pick givers g'
                      newGivers        = delete nextGiver givers
                  in  run nextGiver g'' st
                        { givers      = newGivers
                        , recipients  = newRecipients
                        , assignments = newAssignments
                        }

-- Convenience wrapper: get a StdGen from IO, then run the pure generator
secretSantaIO :: Int -> IO [(Int, Int)]
secretSantaIO n = do
  rng <- getStdGen
  let (pairs, _) = secretSanta n rng
  return pairs
